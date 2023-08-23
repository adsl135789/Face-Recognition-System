import os,sys
import face_recognition
import cv2
import pickle
import time

origin_face_list = []


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
	new_identity["isSupervisor"] = False
	new_identity["encode"] = face_encodings
	print(new_identity)

	return new_identity

def register():
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
			print(origin_face_list)
			pickle.dump(origin_face_list, f)
			img_name = "faces/{}.jpg".format(new_identity["name"])
			cv2.imwrite(img_name, pic)
			print("{} written!".format(img_name))


def remove_identiy():
	global origin_face_list
	try:
		with open('faces.pickle', 'rb') as f:
			origin_face_list = pickle.load(f)
	except FileNotFoundError:
		print("file is not existed.")
		return
	print("all the name in the database:")
	for face in origin_face_list:
		print(face["name"])
	remove_name = input("enter the name you want to remove:")

	for face in origin_face_list:
		try:
			if face["name"] == remove_name:
				origin_face_list.remove(face)
				print(f"{remove_name} has been deleted.")
		except ValueError:
			print(f"{remove_name} doesn't find in the list.")
			return

	with open('faces.pickle', 'wb') as f:
			pickle.dump(origin_face_list, f)

	remove_img_name = f"{remove_name}.jpg"
	remove_img_path = os.getcwd()
	full_path = os.path.join(remove_img_path, "faces", remove_img_name)


	try:
		os.remove(full_path)
		print(f"{remove_name}\'s image has been deleted")
	except FileNotFoundError:
		print(f"{remove_name}'s image not fund in the list.")
	except Exception as e:
		print(f"Error Occured : {e}")


if __name__ == '__main__':
	register()
	remove_identiy()