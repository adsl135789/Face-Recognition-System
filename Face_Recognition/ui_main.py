import sys
import cv2
import os
import datetime
import platform
import configparser
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from ui_view import Ui_MainWindow
from models.faceRecognition import FaceRecognition
from models.relay_ctl import RelayCtl

config = configparser.ConfigParser()

config_path = os.path.join(os.getcwd(), "data/config.ini")
config.read(config_path)

door_num = int(config['door']['door_number'])

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        # self.video_capture = None
        self.video_idx = 0
        try:
            if platform.system() == "Linux":
                self.video_capture = cv2.VideoCapture(self.video_idx)
            elif platform.system() == "Darwin":
                self.video_capture = cv2.VideoCapture(self.video_idx)
            else:
                self.video_capture = cv2.VideoCapture(self.video_idx, cv2.CAP_DSHOW)
        except Exception as e:
            print(e)
        ret, self.frame = self.video_capture.read()
        if not ret:
            sys.exit("video open failed") 
        # set Timer
        self.ui.timer = QTimer(self.main_win)
        self.ui.timer.timeout.connect(self.update_frame)
        self.openCamera()

        self.ui.timer_recognition = QTimer(self.main_win)
        self.ui.timer_recognition.timeout.connect(self.rec)
        self.ui.timer_recognition.start(3000)

        self.fr = FaceRecognition(0.45)

        self.relayCtl = RelayCtl()

    def rec(self):
        self.ui.name_content.setText("")
        self.ui.time_content.setText("")
        capture, face_data = self.fr.run_recognition(self.frame)
        rgb_image = cv2.cvtColor(capture, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
        label = self.ui.left_labelWC
        pixmap = QPixmap.fromImage(image)
        label_width = label.width()
        label_height = label.height()
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatioByExpanding)
        label.setAlignment(Qt.AlignCenter)
        label.setPixmap(pixmap)

        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        name_content = ''
        if face_data:
            for face in face_data:
                name_content += f'{face["name"]} '
                #  開門
                if face['permission']:
                    if face['permission'][door_num] and door_num == 0:
                        self.relayCtl.turn_on()
                        print("Open the Entrance")
                    elif face['permission'][door_num] and door_num == 1:
                        self.relayCtl.turn_off()
                        print("Open the Meeting Room")
            self.ui.time_content.setText(formatted_datetime)
            self.ui.name_content.setText(name_content)

    def openCamera(self):
        if self.video_capture is None:
            if platform.system() == "Linux":
                self.video_capture = cv2.VideoCapture(self.video_idx)
            elif platform.system() == "Darwin":
                self.video_capture = cv2.VideoCapture(self.video_idx)
            else:
                self.video_capture = cv2.VideoCapture(self.video_idx, cv2.CAP_DSHOW)
        self.ui.timer.start(30)

    def update_frame(self):
        if self.video_capture is not None:
            ret, self.frame = self.video_capture.read()
            if ret:
                image = cv2.resize(self.frame, (500, 500))
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
                label = self.ui.right_labelWC
                pixmap = QPixmap.fromImage(image)
                label_width = label.width()
                label_height = label.height()
                pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatioByExpanding)
                label.setAlignment(Qt.AlignCenter)
                label.setPixmap(pixmap)

    def show(self):
        self.main_win.show()

    def close(self):
        self.ui.timer.stop()
        self.ui.timer_recognition.stop()
        self.video_capture.release()
        self.relayCtl.close()
        cv2.destroyAllWindows()
        app.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    if app.exec_() is False:
        main_win.close()
        sys.exit(app.exec_())
