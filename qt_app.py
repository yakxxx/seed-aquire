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
from filters.calibrate_reddot import CalibrateRedDotFilter
from filters.separate_object import SeparateObjectFilter
from filters.base_filter import MetaImg

   
class App(QApplication):     
     
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.on_frame)
        self.video_widget = None
        self.calib_filter = CalibrateRedDotFilter({'dims': (4,4),
                                   'square_size_in_mm': 5})
        self.sep_filter = SeparateObjectFilter()
        self.meta_img = None
        self._frame_count = 0
        
    def set_video_widget(self, video_widget):
        self.video_widget = video_widget 
        
    def on_frame(self):
        ret, frame = self.cam.read()
        if ret:
            vis = frame.copy()
            vis_small = self._downscale(vis)
            if self._frame_count % 15 == 0:
                self.meta_img = MetaImg(vis_small, {})
                self.calib_filter(self.meta_img)
                self.sep_filter(self.meta_img)
                self._frame_count = 0
            if self.meta_img.meta.get('ellipsis', None):
                print('w', self.meta_img.meta['ellipsis'][1][0] * self.meta_img.meta['mm_on_px'],
                      'h', self.meta_img.meta['ellipsis'][1][1] * self.meta_img.meta['mm_on_px'])
                cv2.ellipse(vis_small, self.meta_img.meta['ellipsis'], (0,255,0))
            if self.meta_img.meta.get('red_dot_ellipsis', None):
                cv2.ellipse(vis_small, self.meta_img.meta['red_dot_ellipsis'], (0,0,255))
            
            self.video_widget.push_frame(vis_small)
            self._frame_count += 1
        else:
            self._reset_cam()
             


    def start(self):
        assert(self.video_widget)
        self._reset_cam()
        self._timer.start(50)
        
    def _reset_cam(self):
        self.cam = cv2.VideoCapture(1)
        self.cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
        self.cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 1024) 
   
    def _downscale(self, img):
        h, w, d = img.shape
        img2 = np.zeros((h >> 2, w >> 2, d), dtype=np.uint8)
        for i in xrange(0, h, 4):
            for j in xrange(0, w, 4):
                img2[i >> 2][j >> 2] = img[i][j]
        return img2
     
if __name__ == '__main__':
    app = App(sys.argv)
    form = MainWindow()
    app.set_video_widget(form.video_widget)
    app.start()
    form.show()
    sys.exit(app.exec_())
