import face_recognition
import sys, os
import configparser
import cv2
import database_ctrl

config = configparser.ConfigParser()
config.read("data/config.ini")
try:
    db = database_ctrl.Database(
        host=config["database"]["host"],
        password=config["database"]["password"],
        user=config["database"]["user"],
        database=config["database"]["database"]
    )
except Exception as e:
    print(e)
    sys.exit("Connecting to the database failed!!")

db.create_table()

path = os.getcwd()
filenames = os.listdir("faces_jpg")

for idx,filename in enumerate(filenames):
    frame = cv2.imread(os.path.join(path,"faces_jpg",filename))
    identity_json = {}
    identity_json["name"] = f"person{idx}"
    identity_json["id"] = f'{idx}'
    small_pic = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_pic = cv2.cvtColor(small_pic, cv2.COLOR_BGR2RGB)  # change frame to RGB
    face_locations = face_recognition.face_locations(rgb_pic)
    face_encodings = face_recognition.face_encodings(rgb_pic, face_locations, model='small')
    identity_json["encode"] = face_encodings[0].tolist()
    identity_json["isSupervisor"] = False
    identity_json["permission"] = [True,False]
    print(f"person{idx} stored completed")
    db.insert_data(f"person{idx}",identity_json)
    # if idx == 0: break




