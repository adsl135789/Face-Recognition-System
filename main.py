import face_recognition
import os
import sys
import cv2
import math
import time
import numpy as np
import pickle
import threading

script_dir = os.getcwd()
module_path = os.path.join(script_dir, 'Silent-Face-Anti-Spoofing')
sys.path.append(module_path)


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
    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f'faces/{image}')
            face_encoding = face_recognition.face_encodings(face_image, model='small')[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)

    # Read from the data file
    def encode_faces1(self):
        with open("faces.pickle", 'rb') as f:
            self.known_face_list = pickle.load(f)
        for know_face in self.known_face_list:
            self.known_face_encodings.append(self.known_face["encode"][0])
            self.known_face_names.append(self.known_face["name"])

    def recognition(self, rgb_small_frame):
        # Find all faces in the current frame
        self.face_locations = face_recognition.face_locations(rgb_small_frame)

        # self.real_face = []
        # model_dir = os.path.join(os.getcwd(),"Silent-Face-Anti-Spoofing","resources","anti_spoof_models")

        # for idx, face_location in enumerate(self.face_locations):
        # 	top,right,bottom,left = face_location
        # 	face_image = rgb_small_frame[top:bottom, left:right]

        # 	label = test(
        # 		image = face_image,
        # 		model_dir = model_dir,
        # 		device_id = 0
        # 		)
        # 	self.real_face.append(label)

        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations, model='small')
        self.face_names = []
        for face_encoding in self.face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, self.tolerance)
            name = "Unknown"
            confidence = 'Unknown'

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
                confidence = face_confidence(face_distances[best_match_index])
            self.face_names.append(f'{os.path.splitext(name)[0]} ({confidence})')
            print(name, confidence)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        # wait for the camera for warm up
        time.sleep(2.0)
        # used to record the time when we processed last frame
        prev_frame_time = 0

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        n = 30
        frame_count = 0

        while True:
            ret, frame = video_capture.read()

            # Calculating the fps
            new_frame_time = time.time()
            fps = 1 / (new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time

            # converting the fps into integer
            fps = str(int(fps))
            cv2.putText(frame, fps, (8, 20), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 1)
            if frame_count % n == 0:
                # Resize and change the frame to RGB
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)  # change frame to RGB
                # self.is_running = True
                # p1 = threading.Thread(target=self.recognition, args=(rgb_small_frame,))
                # p1.start()
                self.recognition(rgb_small_frame)
            frame_count += 1

            # Display annotations
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # if real == 1:
                # 	cv2.rectangle(frame, (left,top), (right, bottom), (0,255,0), 2)
                # 	cv2.rectangle(frame, (left,bottom  ), (right, bottom+25), (0,255,0), -1)
                # else:
                # 	cv2.rectangle(frame, (left,top), (right, bottom), (0,0,255), 2)
                # 	cv2.rectangle(frame, (left,bottom  ), (right, bottom+25), (0,0,255), -1)
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom), (right, bottom + 25), (0, 0, 255), -1)
                cv2.putText(frame, name, (left + 6, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

            cv2.imshow('Face Recognition', frame)

            k = cv2.waitKey(1)

            if k % 256 == 27:
                # ESC pressed, exit.
                print("Escape hit, closing...")
                break

        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition(0.5)
    fr.run_recognition()
