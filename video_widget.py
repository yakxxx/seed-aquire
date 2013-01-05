# coding=utf8

import cv2
import numpy as np
import sys


from PyQt4.QtCore import QPoint, QTimer
from PyQt4.QtGui import QApplication, QImage, QPainter, QWidget, QLabel, QPixmap


class CvQImage(QImage):
    def __init__(self, arr):
        h, w = arr.shape[:2]
        arr = arr.astype(np.uint32)
        self.flat = (255 << 24 | arr[:,:,2] << 16 | arr[:,:,1] << 8 | arr[:,:,0])
        self.flat = self.flat.astype(np.uint32)
        super(CvQImage,self).__init__(self.flat, w, h, QImage.Format_RGB32)


class VideoWidget(QWidget):
    """ A class for rendering video coming from OpenCV """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
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
