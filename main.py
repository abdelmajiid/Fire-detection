import os
import random
import sys
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5 import QtGui
from PyQt5.QtMultimedia import QCameraImageCapture
from qtpy.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QImage, QPixmap
from fire_detection.mainwindow import Ui_MainWindow
import subprocess


count = 0


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("fire_detection/Black Logo.svg"))
        self.ui.label_13.setPixmap(QtGui.QPixmap("fire_detection/Asset 1.svg"))
        self.ui.start_cam_button.clicked.connect(self.start_camera)
        # self.ui.view_all_button.clicked.connect(self.do_something)
        self.ui.take_pic_button.clicked.connect(self.capture_image)

    def do_something(self):
        i = random.randint(1, 2)
        if i == 1:
            self.ui.label_video.hide()
        else:
            self.ui.label_video.show()

    def start_camera(self):
        self.camera = cv2.VideoCapture(0)
        while True:
            ret, frame = self.camera.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.ui.label_video.setPixmap(QPixmap.fromImage(image))
            QApplication.processEvents()

    def capture_image(self):
        global count
        # Capture the current frame
        ret, frame = self.camera.read()
        self.camera.release()

        # Save the captured frame to a file
        file_path = "D:/Workspaces/Qt designer/Fire/fire_detection/yolov5/image" + str(count) + ".jpg"
        cv2.imwrite(file_path, frame)
        # subprocess.run(["python", "fire_detection/yolov5/detect.py", "--weights fire_detection/yolov5/_best3.pt",
        # "--source fire_detection/yolov5/image" + str(count) + ".jpg"])
        # result = subprocess.run("python detect.py --weights _best3.pt --source image" + str(count) + ".jpg", shell=True, capture_output=True, text=True)
        result = subprocess.run(["python", "fire_detection/yolov5/detect.py", "--weights fire_detection/yolov5/_best3.pt", "--source fire_detection/yolov5/image" + str(count) + ".jpg"], shell=True, capture_output=True, text=True)
        # process = subprocess.Popen(["python", "fire_detection/yolov5/detect.py"], stdin=subprocess.PIPE,
        # stdout=subprocess.PIPE, stderr=subprocess.PIPE) output, error = process.communicate(input=b"--weights
        # best3.pt , --source  image{str(count)}.jpg") print(output.decode()) print(error.decode())
        print(result.stdout)
        count += 1
        # second_path = "D:/Workspaces/Qt designer/Fire/fire_detection/yolov5/runs/detect/"
        self.start_camera()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
