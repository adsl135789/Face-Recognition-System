import face_recognition
import os
import sys
import cv2
import math
import time
import numpy as np
import pickle

# script_dir = os.getcwd()
# module_path = os.path.join(script_dir, 'Silent-Face-Anti-Spoofing')
# sys.path.append(module_path)


def face_confidence(face_distance, face_match_threshold=0.6):
    rg = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (rg * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    def __init__(self, tolerance=0.4):
        self.tolerance = tolerance
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.real_face = []
        self.known_face_list = []
        self.known_face_names = []
        self.known_face_encodings = []
        self.process_current_frame = True
        self.encode_faces()

    # Read from the pictures directroy
    # def encode_faces(self):
    #     for image in os.listdir('faces'):
    #         face_image = face_recognition.load_image_file(f'faces/{image}')
    #         face_encoding = face_recognition.face_encodings(face_image, model='small')[0]
    #         self.known_face_encodings.append(face_encoding)
    #         self.known_face_names.append(image)

    # Read from the data file
    def encode_faces(self):
        pickle_path = os.path.join(os.getcwd(),"Face_register_UI","pythonfile","faces.pickle")
        with open(pickle_path, 'rb') as f:
            self.known_face_list = pickle.load(f)
        for known_face in self.known_face_list:
            self.known_face_encodings.append(known_face["encode"][0])
            self.known_face_names.append(known_face["name"])

    def recognition(self, rgb_small_frame):
        self.known_face_names = []
        self.known_face_encodings = []
        self.encode_faces()
        print(f"{self.known_face_names=}")
        # Find all faces in the current frame
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations, model='small')
        self.face_names = []
        name = None
        for face_encoding in self.face_encodings:
            name = "Unknown"
            confidence = 'Unknown'
            # print(f"{self.known_face_encodings=}")
            if not self.known_face_encodings:
                return name

            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, self.tolerance)

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
                confidence = face_confidence(face_distances[best_match_index])
            self.face_names.append(f'{os.path.splitext(name)[0]}')
            print(name)
        return name

    def run_recognition(self):
        self.video_capture = cv2.VideoCapture(0)
        ret, frame = self.video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)  # change frame to RGB
        name = self.recognition(rgb_small_frame)
        # Display annotations
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom), (right, bottom + 45), (0, 0, 255), -1)
            cv2.putText(frame, name, (left + 6, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        cv2.resize(frame,(280,280))
        return frame, self.face_names


if __name__ == '__main__':
    fr = FaceRecognition(0.5)
    fr.run_recognition()
