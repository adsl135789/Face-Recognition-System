import face_recognition
import numpy as np
import configparser
import sys,os
from models.database_ctrl import Database

config = configparser.ConfigParser()
config_path = os.path.join(os.getcwd(), "data/config.ini")
config.read(config_path)

try:
    db = Database(
        host=config["database"]["host"],
        password=config["database"]["password"],
        user=config["database"]["user"],
        database=config["database"]["database"]
    )
except Exception as e:
    print("Error:", e)
    sys.exit("Connecting to the database failed!!")


class FaceRecognition:
    def __init__(self, tolerance=0.4):
        self.tolerance = tolerance
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.known_face_list = []
        self.known_face_permission = []
        self.known_face_names = []
        self.known_face_encodings = []
        self.process_current_frame = True

    # Read from the data file
    def encode_faces(self):
        try:
            self.known_face_list = db.read_data()

            for known_face in self.known_face_list:
                # for i in range(len(known_face['encode'])):  # 還原encode的type
                #     known_face['encode'][i] = np.array(known_face['encode'][i])

                self.known_face_encodings.append(np.array(known_face["encode"]))
                self.known_face_permission.append(known_face["permission"])
                self.known_face_names.append(known_face["name"])
        except Exception as e:
            print(f"{e} occured")

    def clearData(self):
        self.known_face_permission = []
        self.known_face_names = []
        self.known_face_encodings = []
        self.face_names = []
        self.encode_faces()

    def recognition(self, rgb_small_frame):
        self.clearData()
        print(f"{self.known_face_names=}")
        # Find all faces in the current frame
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations, model='small')
        face_data = {"name": "", "permission": []}
        if not self.face_encodings:  # 若無偵測到人
            print("There is no anyone in the frame. Return []")
            return self.face_names
        if not self.known_face_encodings:
            print("Database haven't register user. Return EMPTY")
            return "EMPTY"

        for face_encoding in self.face_encodings:
            face_data["name"] = "Unknown"

            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, self.tolerance)

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                face_data["name"] = self.known_face_names[best_match_index]
                face_data["permission"].append(self.known_face_permission[best_match_index])
            print(f"detect identity = {face_data}")
            self.face_names.append(face_data)
        return self.face_names

    # def recognition(self, rgb_small_frame):
    #     self.known_face_names = []
    #     self.known_face_encodings = []
    #     self.encode_faces()
    #     print(f"{self.known_face_names=}")
    #     # Find all faces in the current frame
    #     self.face_locations = face_recognition.face_locations(rgb_small_frame)
    #     self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations, model='small')
    #     self.face_names = []
    #     name = None
    #     for face_encoding in self.face_encodings:
    #         name = "Unknown"
    #         confidence = 'Unknown'
    #         print(f"{self.known_face_encodings=}")
    #         if not self.known_face_encodings:
    #             return name
    #
    #         matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, self.tolerance)
    #
    #         face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
    #         best_match_index = np.argmin(face_distances)
    #
    #         if matches[best_match_index]:
    #             name = self.known_face_names[best_match_index]
    #             # confidence = face_confidence(face_distances[best_match_index])
    #         self.face_names.append(f'{os.path.splitext(name)[0]} ({confidence})')
    #         print(name, confidence)
    #     return name

    # def run_recognition(self):
    #     video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #
    #     # wait for the camera for warm up
    #     time.sleep(2.0)
    #     # used to record the time when we processed last frame
    #     prev_frame_time = 0
    #
    #     if not video_capture.isOpened():
    #         sys.exit('Video source not found...')
    #
    #     n = 30
    #     frame_count = 0
    #
    #     while True:
    #         ret, frame = video_capture.read()
    #
    #         # Calculating the fps
    #         new_frame_time = time.time()
    #         fps = 1 / (new_frame_time - prev_frame_time)
    #         prev_frame_time = new_frame_time
    #
    #         # converting the fps into integer
    #         fps = str(int(fps))
    #         cv2.putText(frame, fps, (8, 20), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 1)
    #         if frame_count % n == 0:
    #             # Resize and change the frame to RGB
    #             small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    #             rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)  # change frame to RGB
    #             # self.is_running = True
    #             # p1 = threading.Thread(target=self.recognition, args=(rgb_small_frame,))
    #             # p1.start()
    #             self.recognition(rgb_small_frame)
    #         frame_count += 1
    #
    #         # Display annotations
    #         for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
    #             top *= 4
    #             right *= 4
    #             bottom *= 4
    #             left *= 4
    #
    #             # if real == 1:
    #             # 	cv2.rectangle(frame, (left,top), (right, bottom), (0,255,0), 2)
    #             # 	cv2.rectangle(frame, (left,bottom  ), (right, bottom+25), (0,255,0), -1)
    #             # else:
    #             # 	cv2.rectangle(frame, (left,top), (right, bottom), (0,0,255), 2)
    #             # 	cv2.rectangle(frame, (left,bottom  ), (right, bottom+25), (0,0,255), -1)
    #             cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    #             cv2.rectangle(frame, (left, bottom), (right, bottom + 25), (0, 0, 255), -1)
    #             cv2.putText(frame, name, (left + 6, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
    #
    #         cv2.imshow('Face Recognition', frame)
    #
    #         k = cv2.waitKey(1)
    #
    #         if k % 256 == 27:
    #             # ESC pressed, exit.
    #             print("Escape hit, closing...")
    #             break
    #
    #     video_capture.release()
    #     cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition(0.5)
    # fr.run_recognition()
