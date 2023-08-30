import face_recognition
import cv2
import numpy as np
from Face_Recognition.models.database_ctrl import Database
import configparser
import sys

config = configparser.ConfigParser()
config.read("data/config.ini")
try:
    db = Database(
        host=config["database"]["host"],
        password=config["database"]["password"],
        user=config["database"]["user"],
        database=config["database"]["database"]
    )
except Exception as e:
    print(e)
    sys.exit("Connecting to the database failed!!")


class FaceRecognition:
    def __init__(self, tolerance=0.4):
        self.tolerance = tolerance
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.real_face = []
        self.known_face_list = []
        self.known_face_permission = []
        self.known_face_names = []
        self.known_face_encodings = []
        self.process_current_frame = True
        self.encode_faces()


    # Read from the data file
    def encode_faces(self):
        self.known_face_list = db.read_data()

        for known_face in self.known_face_list:
            for i in range(len(known_face['encode'])):  # 還原encode的type
                known_face['encode'][i] = np.array(known_face['encode'][i])
            self.known_face_encodings.append(known_face["encode"][0])
            self.known_face_names.append(known_face["name"])
            self.known_face_permission.append(known_face["permission"])

    def clearData(self):
        self.known_face_permission = []
        self.known_face_names = []
        self.known_face_encodings = []
        self.face_names = []
        self.encode_faces()

    def recognition(self, rgb_small_frame):
        self.clearData()
        # print(f"{self.known_face_names=}")
        # Find all faces in the current frame
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations, model='small')
        if not self.face_encodings:  # 若無偵測到人
            print("There is no anyone in the frame. Return []")
            return False
        if not self.known_face_encodings:
            print("Database haven't register user. Return EMPTY")
            return False

        for idx,face_encoding in enumerate(self.face_encodings):
            face_data = {"name": "Unknown", "permission": []}

            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, self.tolerance)

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                face_data["name"] = self.known_face_names[best_match_index]
                face_data["permission"].append(self.known_face_permission[best_match_index])
            print(f"detect identity = {face_data}\n")
            self.face_names.append(face_data)
        return self.face_names

    def run_recognition(self, frame):

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)  # change frame to RGB
        result = self.recognition(rgb_small_frame)
        # Display annotations
        if not result:
            pass
        else:
            for (top, right, bottom, left), face in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                if face["name"] != "Unknown":
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 5)
                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 5)

        cv2.resize(frame,(250,250))

        return frame, result


if __name__ == '__main__':
    fr = FaceRecognition(0.5)
    fr.run_recognition()
