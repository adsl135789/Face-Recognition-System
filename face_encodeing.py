import os,sys
import face_recognition
import cv2
import pickle
import time

origin_face_list = []
known_face_list = []

def encode_faces(self):
	for image in os.listdir('faces'):
		face_image = face_recognition.load_image_file(f'faces/{image}')
		face_encoding = face_recognition.face_encodings(face_image, model='large')[0]

		self.known_face_encodings.append(face_encoding)
		self.known_face_names.append(image)

def take_pic():
	# take a picture from webcam
	video_capture = cv2.VideoCapture(0)

	while True:
		ret, pic = video_capture.read()
		cv2.imshow('Face Recognition System', pic)

		k = cv2.waitKey(1)
		if k%256 == 27:
			# ESC pressed
			print("Escape hit, closing...")
			sys.exit()
		elif k%256 == 32:
			# SPACE pressed
			video_capture.release()

			cv2.destroyAllWindows()
			return pic


	video_capture.release()
	cv2.destroyAllWindows()

def encoding(pic,encode_model='small'):
	new_identity = {}
	small_pic = cv2.resize(pic, (0, 0), fx=0.25, fy=0.25)
	rgb_pic = cv2.cvtColor(small_pic, cv2.COLOR_BGR2RGB)  # change frame to RGB

	# Find all faces in the current frame

	face_locations = face_recognition.face_locations(rgb_pic)

	face_encodings = face_recognition.face_encodings(rgb_pic, face_locations, model=encode_model)



	new_identity["name"] = input("enter name:")
	new_identity["ID"] = input("enter ID:")
	new_identity["encode"] = face_encodings
	print(new_identity)

	return new_identity

def main():
	global origin_face_list
	pic = take_pic()
	new_identity = encoding(pic)
	try:
		with open('faces.pickle', 'rb') as f:
			origin_face_list = pickle.load(f)
	except FileNotFoundError:
		print("file is not existed.")
	# if new identity has been regisitered, close this program.
	if new_identity['name'] in [face['name'] for face in origin_face_list]:
		print("This identity has been existed")
		sys.exit()

	else:
		with open('faces.pickle', 'wb') as f:
			origin_face_list.append(new_identity)
			pickle.dump(origin_face_list, f)
			img_name = "faces/{}.jpg".format(new_identity["name"])
			cv2.imwrite(img_name, pic)
			print("{} written!".format(img_name))


if __name__ == '__main__':
	main()
