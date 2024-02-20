import sys, os
import cv2
import pandas as pd
import threading
import face_recognition
import configparser
import platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDesktopWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from ui_view import Ui_MainWindow
from functools import partial
from models.recognition import FaceRecognition
from models.database_ctrl import Database
from models.socket_signal import SSignal


config = configparser.ConfigParser()
config_path = os.path.join(os.getcwd(),"data/config.ini")
config.read(config_path)

superCode = config['data']['superCode']
video_idx = int(config["data"]["video_idx"])
csv_file_path = config["path"]["csv_file_path"]

try:
    db = Database(
        host=config["database"]["host"],
        password=config["database"]["password"],
        user=config["database"]["user"],
        database=config["database"]["database"]
    )
    db.create_table()
except Exception as e:
    sys.exit(f"Connecting to the database failed!!\nError:{e}")


class FaceMainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()  # 实例化 Ui_MainWindow 类
        self.ui.setupUi(self.main_win)
        self.initUISize()

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
        if platform.system() == "Linux":
            print("Run on Linux")
            self.video_capture = cv2.VideoCapture(video_idx)
        elif platform.system() == "Darwin":
            print("Run on MacOS")
            self.video_capture = cv2.VideoCapture(video_idx)
        else:
            print("Run on Windows")
            self.video_capture = cv2.VideoCapture(video_idx, cv2.CAP_DSHOW)
        self.frame = None

        # set Timer
        self.ui.timer_user = QTimer(self.main_win)
        self.ui.timer_user.timeout.connect(self.update_frame_user)

        self.ui.timer_super = QTimer(self.main_win)
        self.ui.timer_super.timeout.connect(self.update_frame_super)

        self.ui.timer_confirm = QTimer(self.main_win)
        self.ui.timer_confirm.timeout.connect(self.update_frame_confirm)

        self.fr = FaceRecognition(0.40)

    # Set window size to maximum
    def initUISize(self):
        desktop = QDesktopWidget()
        screen_rect = desktop.screenGeometry()
        screen_width = screen_rect.width()
        screen_height = screen_rect.height()
        self.main_win.setWindowTitle("景文科大餐旅系門禁管理系統")
        self.main_win.resize(screen_width, screen_height)

    ###################### Update Each Frame ######################
    def update_frame_user(self):
        if self.video_capture is not None:
            # print("video is open")
            ret, self.frame = self.video_capture.read()
            if ret:
                image = cv2.resize(self.frame, (500, 500))
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)

                pixmap = QPixmap.fromImage(image)
                label = self.ui.user_labelWC
                self.update_label(label, pixmap)
            else:
                sys.exit("Camera access failed!")

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
            else:
                sys.exit("Camera access failed!")

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
            else:
                sys.exit("Camera access failed!")

    def update_label(self, label, pixmap):
        label_width = label.width()
        label_height = label.height()
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatioByExpanding)
        label.setAlignment(Qt.AlignCenter)
        label.setPixmap(pixmap)

    ###################### Camera Operation ######################
    def openCamera(self, label):
        if self.video_capture is None:
            if platform.system() == "Linux":
                self.video_capture = cv2.VideoCapture(video_idx)
            elif platform.system() == "Darwin":
                self.video_capture = cv2.VideoCapture(video_idx)
            else:
                self.video_capture = cv2.VideoCapture(video_idx, cv2.CAP_DSHOW)

        if label == self.ui.user_labelWC:
            print("timer start : user video")
            self.ui.timer_user.start(30)
        elif label == self.ui.super_labelWC:
            print("timer start : supervisor video")
            self.ui.timer_super.start(30)
        elif label == self.ui.cf_labelWC:
            print("timer start : confirm video")
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

        def (self, label):
        if label == self.ui.user_labelWC:
            self.ui.timer_user.stop()
        elif label == self.ui.super_labelWC:
            self.ui.timer_super.stop()
        elif label == self.ui.cf_labelWC:
            self.ui.timer_confirm.stop()
            
        if self.video_capture:
            ret, self.frame = self.video_capture.read()
        else:
            self.open_dialog("Error: access to camera failed")
            self.goHome()
            
        rgb_pic = self.to_rgb(self.frame)
        face_locations = face_recognition.face_locations(rgb_pic)
        if not face_locations:
            self.open_dialog("Detect Failed. Please retake the photo.")
            if label == self.ui.user_labelWC:
                self.ui.timer_user.start()
            elif label == self.ui.super_labelWC:
                self.ui.timer_super.start()
            elif label == self.ui.cf_labelWC:
                self.goConfirm()
            return False
        return True

    def take_and_confirm(self):
        if self.takePhoto(self.ui.cf_labelWC) is False:
            return

        if self.frame is not None:  # 檢查 self.frame 是否為有效圖像
            rgb_small_frame = self.to_rgb(self.frame)

            detect_names = self.fr.recognition(rgb_small_frame)
            detcet_face_num = len(detect_names)
            if detcet_face_num > 1:
                self.open_dialog("Please don't have more than two people in the camara at the same time.")
                self.goConfirm()
                return

            detect_name = detect_names[0]
            print(f"removing {detect_name=}")
            if detect_name["name"] == self.ui.rm_name_lineEdit.text():  # remove own identity
                self.remove_identiy()
                self.goHome()
                return
            elif self.isSupervisor(detect_name["name"]) is True:  # supervisor remove someone's identity
                self.remove_identiy()
                self.goHome()
                return
            elif detect_name["name"] == 'Unknown':  # the person detected is not registered
                self.open_dialog("You haven't register in the database.")
                self.goHome()
                return
            else:  # detect_name != remove_name, and you are not Supervisor,
                self.open_dialog("You can't remove other user.")
                self.goRemove()
                return

        else:
            print("self.frame is empty")
            self.open_dialog("The frame is empty.")
            self.goConfirm()
            return

    def removeAll_confirm(self):
        self.takePhoto(self.ui.cf_labelWC)
        if self.frame is not None:  # 檢查 self.frame 是否為有效圖像
            rgb_small_frame = self.to_rgb(self.frame)
            detect_names = self.fr.recognition(rgb_small_frame)
            for detect_name in detect_names:
                if self.isSupervisor(detect_name["name"]) is True:
                    self.removeAll()
                    self.open_dialog("Remove all of user")
                    self.goHome()
                else:
                    self.goHome()

    ###################### Identity Register ######################
    def user_register(self):
        if self.ui.user_name_lineEdit.text() == "" or self.ui.user_id_label.text() == "":
            self.open_dialog("You must fill in all input fields.")
            return
        if not self.ui.user_perm1.isChecked() and not self.ui.user_perm2.isChecked():
            self.open_dialog("You must fill in all input fields.")
            return
        new_identity = {}
        rgb_pic = self.to_rgb(self.frame)

        # Find all faces in the current frame
        face_locations = face_recognition.face_locations(rgb_pic)
        face_encodings = face_recognition.face_encodings(rgb_pic, face_locations)

        permission = [self.ui.user_perm1.isChecked(), self.ui.user_perm2.isChecked()]
        new_identity["name"] = self.ui.user_name_lineEdit.text()
        new_identity["ID"] = self.ui.user_id_lineEdit.text()
        new_identity["isSupervisor"] = False
        new_identity["permission"] = permission
        new_identity["encode"] = face_encodings

        self.write_data(new_identity, rgb_pic)

    def super_register(self):
        if (self.ui.super_name_lineEdit.text() == "" or
                self.ui.super_id_label.text() == "" or
                self.ui.supervisor_lineEdit_3.text() == ""):
            self.open_dialog("You must fill in all input fields.")
            return
        new_identity = {}
        rgb_pic = self.to_rgb(self.frame)

        # Find all faces in the current frame
        face_locations = face_recognition.face_locations(rgb_pic)
        face_encodings = face_recognition.face_encodings(rgb_pic, face_locations)

        if self.ui.supervisor_lineEdit_3.text() == superCode:
            new_identity["name"] = self.ui.super_name_lineEdit.text()
            new_identity["ID"] = self.ui.super_id_lineEdit.text()
            new_identity["isSupervisor"] = True
            new_identity["permission"] = [True, True]
        else:
            self.open_dialog("Supervisor code is wrong.")
            self.goHome()
            return

        new_identity["encode"] = face_encodings

        self.write_data(new_identity, rgb_pic)

    def write_data(self, new_identity, rgb_small_frame):
        print(new_identity)
        # 修正encode的type nparray to list
        new_identity['encode'] = new_identity['encode'][0].tolist()

        # 檢查是否有人註冊第二次
        if rgb_small_frame is not None:
            detect_names = self.fr.recognition(rgb_small_frame)

            num_people = len(detect_names)
            if detect_names == "EMPTY":  # 如果資料庫沒使用者，直接跳去註冊新使用者
                pass
            elif num_people > 1: # 偵測到超過兩個人，重新拍照
                self.open_dialog("Multiple people detected in the frame. Please ensure there are no other individuals around and move closer.")
                if not new_identity["isSupervisor"]:
                    self.openCamera(self.ui.user_labelWC)
                    self.goUser()
                else:
                    self.openCamera(self.ui.super_labelWC)
                    self.goSupervisor()
                return
            elif num_people == 1: 
                if detect_names[0]["name"] != "Unknown":  # 若讀到的臉有註冊在資料庫中，重新登錄
                    self.open_dialog("You have already registered.")
                    self.goHome()
                    return
                else:  # 註冊成功，寫入host database and csv file, 通知remote database update
                    db.insert_data(new_identity['name'], new_identity)
                    self.write_csv(new_identity)
            
                    signal = SSignal('insert')
                    signal.setParent(self.main_win)
                    signal.start()
            
                    self.open_dialog(f"{new_identity['name']} Registration Completed")
                    self.goHome()
        
            elif num_people == 0:  # 無偵測到人臉，重拍照
                self.open_dialog("Detect Failed. Please Retake the photo.")
                if not new_identity["isSupervisor"]:
                    self.openCamera(self.ui.user_labelWC)
                    self.goUser()
                else:
                    self.openCamera(self.ui.super_labelWC)
                    self.goSupervisor()
                return
        else:
            print("rgb_small_frame is empty")
            self.open_dialog("The frame is empty.")
            self.goHome()
            return

        # # if new identity has been registered, close this program.
        # if db.read_someone_data(new_identity["name"]):
        #     self.open_dialog("This identity has been existed or your name has been registered.")
        #     self.goHome()
        #     return
        # else:

    def write_csv(self, new_identity):
        new_identity.pop("encode")  # remove the column of "encode"
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
        remove_name = self.ui.rm_name_lineEdit.text()
        print(f"{remove_name} has been deleted.")
        self.open_dialog(f"{remove_name} has been deleted.")
        db.delete_data(remove_name)

        signal = SSignal(f'delete {remove_name}')
        signal.setParent(self.main_win)
        signal.start()

        background_thread = threading.Thread(target=self.remove_csv_in_background, args=(remove_name,))
        background_thread.start()

    def remove_csv_in_background(self, remove_name):
        if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
            df = pd.read_csv(csv_file_path)
            for idx, name in enumerate(df['name']):
                if name == remove_name:
                    df = df.drop(idx)

            # 將修改後的 DataFrame 寫回 CSV 檔案
            df.to_csv(csv_file_path, index=False)

            print("已刪除資料並更新 CSV 檔案:", csv_file_path)
        else:
            print("the csv file is empty.")

    def removeAll(self):
        if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
            df = pd.read_csv(csv_file_path)
            for idx, is_super in enumerate(df['isSupervisor']):
                if is_super is False:
                    df = df.drop(idx)

            # 將修改後的 DataFrame 寫回 CSV 檔案
            df.to_csv(csv_file_path, index=False)

            print("已刪除資料並更新 CSV 檔案:", csv_file_path)
        else:
            print("the csv file is empty.")
        db.delete_all_data()

        signal = SSignal('deleteAll')
        signal.setParent(self.main_win)
        signal.start()

    ###################### Switching Page ######################
    def goUser(self):
        self.ui.user_name_lineEdit.setText("")
        self.ui.user_id_lineEdit.setText("")
        self.ui.user_perm1.setChecked(False)
        self.ui.user_perm2.setChecked(False)
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

        # check if database is empty
        if not db.read_data():
            self.open_dialog("The database is empty")
            self.goHome()
            return

        remove_name = self.ui.rm_name_lineEdit.text()

        if db.find_user(remove_name):
            try:
                self.ui.cf_confirmBtn.clicked.disconnect()
            except Exception as e:
                pass
            self.ui.cf_confirmBtn.clicked.connect(self.take_and_confirm)
            self.ui.remStack.setCurrentWidget(self.ui.confirmPage)
            self.openCamera(self.ui.cf_labelWC)
        else:
            print(f"{remove_name} not found in the list.")
            self.open_dialog(f"{remove_name} not fund in the database.")
            self.goRemove()
            return

    def goRemoveAllConfirm(self):

        # Verify if this name exists in the database.
        if not db.read_data():
            self.open_dialog("The database is empty")
            self.goHome()
            return
        # go confirm page and open camera
        try:
            self.ui.cf_confirmBtn.clicked.disconnect()
        except Exception as e:
            pass
        self.ui.cf_confirmBtn.clicked.connect(self.removeAll_confirm)
        self.ui.remStack.setCurrentWidget(self.ui.confirmPage)
        self.openCamera(self.ui.cf_labelWC)

    def goHome(self):
        self.ui.mainStack.setCurrentWidget(self.ui.mainPage)
        self.ui.remStack.setCurrentWidget(self.ui.rmPage)
        self.closeCamera()

    ###################### The Others ######################
    def isSupervisor(self, super_name):
        face = db.read_someone_data(super_name)
        if face:
            face = face[0]
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

    def open_dialog(self, content):
        QMessageBox.information(self.main_win, "Message", content)
        
    def to_rgb(self, frame):
        small_pic = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_pic = cv2.cvtColor(small_pic, cv2.COLOR_BGR2RGB)  # change frame to RGB
        return rgb_pic

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = FaceMainWindow()
    main_win.show()
    sys.exit(app.exec_())
