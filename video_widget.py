# coding=utf8

# Copyright (C) 2011 Saúl Ibarra Corretgé <saghul@gmail.com>
#

# Some inspiration taken from: http://www.morethantechnical.com/2009/03/05/qt-opencv-combined-for-face-detecting-qwidgets/

import cv2.cv as cv
import cv2
import numpy as np
import sys


from PyQt4.QtCore import QPoint, QTimer
from PyQt4.QtGui import QApplication, QImage, QPainter, QWidget, QLabel, QPixmap


class CvQImage(QImage):
    def __init__(self, arr):
        h, w = arr.shape[:2]
        arr = arr.astype(np.uint32)
        self.flat = (255 << 24 | arr[:,:,2] << 16 | arr[:,:,1] << 8 | arr[:,:,0])#.flatten() # pack RGB values
        self.flat = self.flat.astype(np.uint32)
        super(CvQImage,self).__init__(self.flat, w, h, QImage.Format_RGB32)


class VideoWidget(QWidget):
    """ A class for rendering video coming from OpenCV """

    def __init__(self, parent=None):
        QWidget.__init__(self)
        self._image = None
        self._frame = None

    def _build_image(self, frame):
        return CvQImage(frame)

    def paintEvent(self, event):
        if self._image:
            painter = QPainter(self)
            painter.drawImage(QPoint(0, 0), self._image)

    def push_frame(self, frame):
        self._image = self._build_image(frame)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
#    im3 = cv2.imread('tests/lena.jpg')
#    image2 = CvQImage(im3)
#    image = QImage('tests/lena.jpg') 
    widget = VideoWidget()
#    label = QLabel()
#    label.setPixmap(QPixmap.fromImage(image2))
    widget.setWindowTitle('PyQt - OpenCV Test')
    widget.show()

    sys.exit(app.exec_())
