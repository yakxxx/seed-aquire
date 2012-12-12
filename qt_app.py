#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from main_window import MainWindow
import cv2
import cv2.cv as cv   
import numpy as np

from filters.calibrate_chessboard import CalibrateChessFilter
from filters.separate_object import SeparateObjectFilter
from filters.base_filter import MetaImg

   
class App(QApplication):     
     
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.on_frame)
        self.video_widget = None
        self.calib_filter = CalibrateChessFilter({'dims': (4,4),
                                   'square_size_in_mm': 5})
        self.sep_filter = SeparateObjectFilter()
        
    def set_video_widget(self, video_widget):
        self.video_widget = video_widget 
        
    def on_frame(self):
        ret, frame = self.cam.read()
        if ret:
            vis = frame.copy()
            meta_img = MetaImg(vis, {})
            self.calib_filter(meta_img)
            self.sep_filter(meta_img)
            self.video_widget.push_frame(meta_img.img)
            


    def start(self):
        assert(self.video_widget)
        self.cam = cv2.VideoCapture(0)
        self._timer.start(50)
     
     
if __name__ == '__main__':
    app = App(sys.argv)
    form = MainWindow()
    app.set_video_widget(form.video_widget)
    app.start()
    form.show()
    sys.exit(app.exec_())
