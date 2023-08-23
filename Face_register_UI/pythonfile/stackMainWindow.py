import sys, os
import cv2
import pandas as pd
import pickle
import threading
import face_recognition
import configparser
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from stack_main import Ui_MainWindow
from functools import partial
from recognition import FaceRecognition

config = configparser.ConfigParser()
config.read("config.ini")
superCode = config['data']['superCode']
confirmLimit = config['data']['confirmLimit']


class FaceMainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()  # 实例化 Ui_MainWindow 类
        self.ui.setupUi(self.main_win)

        # 設定每個stackWidget的初始頁面
        self.ui.mainStack.setCurrentWidget(self.ui.mainPage)
        self.ui.remStack.setCurrentWidget(self.ui.rmPage)

        # 設定main page的button
        self.ui.userBtn.clicked.connect(self.goUser)
        self.ui.superBtn.clicked.connect(self.goSupervisor)
        self.ui.rmBtn.clicked.connect(self.goRemove)

        # 設定user page的button
        self.ui.user_homeBtn.clicked.connect(self.goHome)
        self.ui.user_takeBtn.clicked.connect(partial(self.takePhoto, self.ui.user_labelWC))
        self.ui.user_retakeBtn.clicked.connect(partial(self.openCamera, self.ui.user_labelWC))
        self.ui.user_okBtn.clicked.connect(self.user_register)

        # 設定supervisor page的button
        self.ui.super_homeBtn.clicked.connect(self.goHome)
        self.ui.super_takeBtn.clicked.connect(partial(self.takePhoto, self.ui.super_labelWC))
        self.ui.super_retakeBtn.clicked.connect(partial(self.openCamera, self.ui.super_labelWC))
        self.ui.super_okBtn.clicked.connect(self.super_register)

        # 設定remove page的button
        self.ui.rm_homeBtn.clicked.connect(self.goHome)
        self.ui.rm_rmBtn.clicked.connect(self.goConfirm)
        self.ui.rm_rmAllBtn.clicked.connect(self.goRemoveAllConfirm)

        # 設定confirm page的button
        self.ui.cf_homeBtn.clicked.connect(self.goHome)

        # init video variables
        self.video_capture = None
        self.frame = None

        # set Timer
        self.ui.timer_user = QTimer(self.main_win)
        self.ui.timer_user.timeout.connect(self.update_frame_user)

        self.ui.timer_super = QTimer(self.main_win)
        self.ui.timer_super.timeout.connect(self.update_frame_super)

        self.ui.timer_confirm = QTimer(self.main_win)
        self.ui.timer_confirm.timeout.connect(self.update_frame_confirm)

        self.fr = FaceRecognition(0.425)

        self.confirmCount = 0

    ###################### Update Each Frame ######################
    def update_frame_user(self):
        if self.video_capture is not None:
            ret, self.frame = self.video_capture.read()
            if ret:
                image = cv2.resize(self.frame, (500, 500))
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)

                pixmap = QPixmap.fromImage(image)
                label = self.ui.user_labelWC
                self.update_label(label, pixmap)

    def update_frame_super(self):
        if self.video_capture is not None:
            ret, self.frame = self.video_capture.read()
            if ret:
                image = cv2.resize(self.frame, (500, 500))
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)

                pixmap = QPixmap.fromImage(image)
                label = self.ui.super_labelWC
                self.update_label(label, pixmap)

    def update_frame_confirm(self):
        if self.video_capture is not None:
            ret, self.frame = self.video_capture.read()
            if ret:
                image = cv2.resize(self.frame, (500, 500))
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)

                pixmap = QPixmap.fromImage(image)
                label = self.ui.cf_labelWC
                self.update_label(label, pixmap)

    def update_label(self, label, pixmap):
        label_width = label.width()
        label_height = label.height()
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatioByExpanding)
        label.setAlignment(Qt.AlignCenter)
        label.setPixmap(pixmap)

    ###################### Camera Operation ######################
    def openCamera(self, label):
        if self.video_capture is None:
            self.video_capture = cv2.VideoCapture(0)  # 摄像头索引，通常是0

        if label == self.ui.user_labelWC:
            self.ui.timer_user.start(30)
        elif label == self.ui.super_labelWC:
            self.ui.timer_super.start(30)
        elif label == self.ui.cf_labelWC:
            self.ui.timer_confirm.start(30)

    def closeCamera(self):
        if self.video_capture is not None:
            self.video_capture.release()
            self.ui.timer_user.stop()
            self.ui.user_labelWC.clear()  # 清除 QLabel 中的图像
            self.ui.timer_super.stop()
            self.ui.super_labelWC.clear()  # 清除 QLabel 中的图像
            self.ui.timer_confirm.stop()
            self.ui.cf_labelWC.clear()  # 清除 QLabel 中的图像
            self.video_capture = None

    def takePhoto(self, label):
        if label == self.ui.user_labelWC:
            self.ui.timer_user.stop()
        elif label == self.ui.super_labelWC:
            self.ui.timer_super.stop()
        elif label == self.ui.cf_labelWC:
            self.ui.timer_confirm.stop()
        ret, self.frame = self.video_capture.read()

    def take_and_confirm(self):
        self.ui.timer_confirm.stop()
        ret, self.frame = self.video_capture.read()
        if self.frame is not None: # 檢查 self.frame 是否為有效圖像
            small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            detect_name = self.fr.recognition(rgb_small_frame)
            print(f"{detect_name=}")
            if detect_name == self.ui.rm_name_lineEdit.text():  # remove own identity
                self.remove_identiy()
                self.goHome()
                return
            elif self.isSupervisor(detect_name) is True:  # supervisor remove someone's identity
                self.remove_identiy()
                self.goHome()
                return
            elif detect_name is None:  # no detect anyone
                self.open_dialog("Detect Failed. Please Retake the photo.")
            elif detect_name == 'Unknown':  # the person detected is not registered
                self.open_dialog("The detected identity is not in the database.")
            else:  # detect_name != remove_name, and you are not Supervisor,
                self.open_dialog("You can't remove other user.")
            # failed confirm
            self.goConfirm()
            self.confirmCount += 1
            if self.confirmCount == confirmLimit:
                self.open_dialog(f"Failed identity verification for {confirmLimit} consecutive attempts.")
                self.confirmCount = 0
                self.goHome()
                return
        else:
            print("self.frame is empty")
            self.open_dialog("The frame is empty.")
            self.goConfirm()
            return

    def removeAll_confirm(self):
        self.ui.timer_confirm.stop()
        if self.video_capture:
            ret, self.frame = self.video_capture.read()
        if self.frame is not None:  # 檢查 self.frame 是否為有效圖像
            small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            detect_name = self.fr.recognition(rgb_small_frame)
            if self.isSupervisor(detect_name) is True:
                self.removeAll()
                self.open_dialog("Remove all of user")
                self.goHome()
            else:
                self.open_dialog("Confirm fail.")
                self.goHome()

    ###################### Identity Register ######################
    def user_register(self):
        if self.ui.user_name_lineEdit.text() == "" or self.ui.user_id_label.text() == "":
            self.open_dialog("You must fill in all input fields.")
            return
        new_identity = {}
        small_pic = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
        rgb_pic = cv2.cvtColor(small_pic, cv2.COLOR_BGR2RGB)  # change frame to RGB

        # Find all faces in the current frame
        face_locations = face_recognition.face_locations(rgb_pic)
        face_encodings = face_recognition.face_encodings(rgb_pic, face_locations)

        new_identity["name"] = self.ui.user_name_lineEdit.text()
        new_identity["ID"] = self.ui.user_id_lineEdit.text()
        new_identity["isSupervisor"] = False
        new_identity["encode"] = face_encodings

        self.write_data(new_identity, rgb_pic)

    def super_register(self):
        if (self.ui.super_name_lineEdit.text() == "" or
                self.ui.super_id_label.text() == "" or
                self.ui.supervisor_lineEdit_3.text() == ""):
            self.open_dialog("You must fill in all input fields.")
            return
        new_identity = {}
        small_pic = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
        rgb_pic = cv2.cvtColor(small_pic, cv2.COLOR_BGR2RGB)  # change frame to RGB

        # Find all faces in the current frame
        face_locations = face_recognition.face_locations(rgb_pic)
        face_encodings = face_recognition.face_encodings(rgb_pic, face_locations)

        if self.ui.supervisor_lineEdit_3.text() == superCode:
            new_identity["name"] = self.ui.super_name_lineEdit.text()
            new_identity["ID"] = self.ui.super_id_lineEdit.text()
            new_identity["isSupervisor"] = True
        else:
            self.open_dialog("Supervisor code is wrong.")
            self.goHome()
            return
        new_identity["encode"] = face_encodings
        self.write_data(new_identity, rgb_pic)

    def write_data(self, new_identity, rgb_small_frame):
        # 檢查是否有人註冊第二次
        if self.frame is not None:
            detect_name = self.fr.recognition(rgb_small_frame)
            print(f'{detect_name=}')
            if detect_name is None:
                self.open_dialog("Detect Failed. Please Retake the photo.")
                self.goHome()
                return
            elif detect_name != "Unknown":
                self.open_dialog("You cannot register twice using different names.")
                if new_identity["isSupervisor"] is False:
                    self.goUser()
                else:
                    self.goSupervisor()
                return
        else:
            print("self.frame is empty")
            self.open_dialog("The frame is empty.")
            self.goHome()
            return

        origin_face_list = []

        try:
            with open('faces.pickle', 'rb') as f:
                origin_face_list = pickle.load(f)
        except Exception as e:
            print("file is not existed or empty.")

        # if new identity has been registered, close this program.
        if new_identity['name'] in [face['name'] for face in origin_face_list]:
            self.open_dialog("This identity has been existed")
        else:
            with open('faces.pickle', 'wb') as f: # 存入pickle檔
                origin_face_list.append(new_identity)
                pickle.dump(origin_face_list, f)
            # img_name = "faces/{}.jpg".format(new_identity["name"])
            # cv2.imwrite(img_name, cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
            self.write_csv(new_identity)
            self.open_dialog(f"{new_identity['name']} Registration Completed")
        self.goHome()

    def write_csv(self, new_identity):
        csv_file_path = 'identity.csv'
        new_identity.pop("encode")  # remove the column of "encode"
        print(f"{new_identity=}")
        df = pd.DataFrame([new_identity])
        if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
            header_flag = False  # 不寫入標題
        else:
            header_flag = True  # 寫入標題
        # 將 DataFrame 寫入 CSV 檔案
        try:
            df.to_csv(csv_file_path, mode='a', index=False, header=header_flag)
        except FileNotFoundError:
            df.to_csv(csv_file_path, index=False)

        print("已追加新資料到 CSV 檔案:", csv_file_path)

    ###################### Identity Remove ######################

    def remove_identiy(self):
        # 刪除pickle檔
        origin_face_list = []
        with open('faces.pickle', 'rb') as f:
            origin_face_list = pickle.load(f)
        remove_name = self.ui.rm_name_lineEdit.text()
        for face in origin_face_list:
            if face["name"] == remove_name:
                origin_face_list.remove(face)
                print(f"{remove_name} has been deleted.")
                self.open_dialog(f"{remove_name} has been deleted.")

        with open('faces.pickle', 'wb') as f:
            print(f"{origin_face_list=}")
            pickle.dump(origin_face_list, f)
        # 刪除照片
        # remove_img_name = f"{remove_name}.jpg"
        # remove_img_path = os.getcwd()
        # full_path = os.path.join(remove_img_path, "faces", remove_img_name)
        # try:
        #     os.remove(full_path)
        #     print(f"{remove_name}\'s image has been deleted")
        # except FileNotFoundError:
        #     print(f"{remove_name} image not fund in the list.")
        # except Exception as e:
        #     print(f"Error Occured : {e}")
        background_thread = threading.Thread(target=self.write_csv_in_background, args=(remove_name,))
        background_thread.start()

    def write_csv_in_background(self, remove_name):
        csv_file_path = 'identity.csv'

        if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
            df = pd.read_csv(csv_file_path)
            print(f"{remove_name=}")
            for idx, name in enumerate(df['name']):
                print(f"{idx=} {name=}")
                if name == remove_name:
                    df = df.drop(idx)


            # 將修改後的 DataFrame 寫回 CSV 檔案
            df.to_csv(csv_file_path, index=False)

            print("已刪除資料並更新 CSV 檔案:", csv_file_path)
        else:
            print("the csv file is empty.")


    def removeAll(self):
        with open('faces.pickle', 'w') as f:
            pass
        with open('identity.csv', 'w') as f:
            pass

        remove_dir = os.path.join(os.getcwd(),'faces')
        for filename in os.listdir(remove_dir):
            file_path = os.path.join(remove_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print('無法刪除 %s. 原因: %s' % (file_path, e))

    ###################### Switching Page ######################
    def goUser(self):
        self.ui.user_name_lineEdit.setText("")
        self.ui.user_id_lineEdit.setText("")
        self.ui.mainStack.setCurrentWidget(self.ui.userPage)
        self.openCamera(self.ui.user_labelWC)

    def goSupervisor(self):
        self.ui.super_name_lineEdit.setText("")
        self.ui.super_id_lineEdit.setText("")
        self.ui.supervisor_lineEdit_3.setText("")
        self.ui.mainStack.setCurrentWidget(self.ui.superPage)
        self.openCamera(self.ui.super_labelWC)

    def goRemove(self):
        self.ui.rm_name_lineEdit.setText("")
        self.ui.mainStack.setCurrentWidget(self.ui.removePage)

    def goConfirm(self):
        # check all the inputs be filled
        if self.ui.rm_name_lineEdit.text() == "":
            self.open_dialog("You must fill in all input fields.")
            return
        # Verify if this name exists in the database.
        try:
            with open('faces.pickle', 'rb') as f:
                origin_face_list = pickle.load(f)
        except FileNotFoundError:
            self.open_dialog("The database is empty")
            self.goHome()
            return

        # if database is empty
        if not origin_face_list:
            self.open_dialog("The database is empty")
            self.goHome()
            return

        remove_name = self.ui.rm_name_lineEdit.text()

        for face in origin_face_list:
            if face["name"] == remove_name:
                self.ui.cf_confirmBtn.clicked.connect(self.take_and_confirm)
                self.ui.remStack.setCurrentWidget(self.ui.confirmPage)
                self.openCamera(self.ui.cf_labelWC)
                break
        # if all face['name'] != remove_name goto following else
        else:
            print(f"{remove_name} not fund in the list.")
            self.open_dialog(f"{remove_name} not fund in the database.")
            self.goRemove()
            return

    def goRemoveAllConfirm(self):
        # Verify if this name exists in the database.
        try:
            with open('faces.pickle', 'rb') as f:
                origin_face_list = pickle.load(f)
        except Exception as e:
            self.open_dialog("The database is empty")
            self.goHome()
            return
        # if database is empty
        if not origin_face_list:
            self.open_dialog("The database is empty")
            self.goHome()
            return
        # go confirm page and open camera
        self.ui.cf_confirmBtn.clicked.connect(self.removeAll_confirm)
        self.ui.remStack.setCurrentWidget(self.ui.confirmPage)
        self.openCamera(self.ui.cf_labelWC)

    def goHome(self):
        self.ui.mainStack.setCurrentWidget(self.ui.mainPage)
        self.ui.remStack.setCurrentWidget(self.ui.rmPage)
        self.closeCamera()

    ###################### The Others ######################
    def isSupervisor(self, super_name):
        try:
            with open('faces.pickle', 'rb') as f:
                origin_face_list = pickle.load(f)
        except FileNotFoundError:
            print("file is not existed.")
            return

        for face in origin_face_list:
            if face['name'] == super_name:
                if face["isSupervisor"] is True:
                    print(f"Confirm Supervisor : {face['name']} .")
                    return True
                else:
                    print("You are not supervisor.")
                    self.open_dialog("You are not supervisor.")
                    return False
        # self.open_dialog("You haven't registered your identity.")
        return False

    def show(self):
        self.main_win.show()

    def open_dialog(self,content):
        QMessageBox.information(self.main_win, "Message", content)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = FaceMainWindow()
    main_win.show()
    sys.exit(app.exec_())
