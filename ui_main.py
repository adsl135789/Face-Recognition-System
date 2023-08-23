import sys, os
import cv2
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from mainWindow import Ui_MainWindow
from faceRecognition import FaceRecognition

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        # self.video_capture = None
        self.frame = None
        self.video_capture = cv2.VideoCapture(0)

        # set Timer
        self.ui.timer = QTimer(self.main_win)
        self.ui.timer.timeout.connect(self.update_frame)
        self.openCamera()

        self.ui.timer_recognition = QTimer(self.main_win)
        self.ui.timer_recognition.timeout.connect(self.rec)
        self.ui.timer_recognition.start(5000)

        self.fr = FaceRecognition(0.425)

    def rec(self):
        self.ui.name_content.setText("")
        self.ui.time_content.setText("")
        capture, names = self.fr.run_recognition()
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

        if names:
            for name in names:
                print(name)
                name_content += f'{name} '
            self.ui.time_content.setText(formatted_datetime)
            self.ui.name_content.setText(name_content)

    def openCamera(self):
        if self.video_capture is None:
            self.video_capture = cv2.VideoCapture(0)  # 摄像头索引，通常是0
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())