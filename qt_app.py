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
        self.video_widget = None
        self.meta_img = None
        self._frame_count = 0
        self.form = None
        self.cam_num = 1
        self._prev_grab_res = (1280, 1024)
        self._snap_grap_res = (2592, 1944)
        self._show_detail = False
        
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.on_frame)
        
        self.calib_filter = CalibrateRedDotFilter({'dims': (4,4),
                                   'square_size_in_mm': 5})
        self.sep_filter = SeparateObjectFilter()
        
    def set_video_widget(self, video_widget):
        self.video_widget = video_widget 
        
    def set_form(self, form):
        self.form = form
        self.form.key_press.connect(self.on_key_press)
        self.form.key_release.connect(self.on_key_release)
        
    def on_key_press(self, key):
        if key and key[0] == 'p':
            self.on_detail_prev_show()
        
    def on_key_release(self, key):
        if key and key[0] == 'p':
            self.on_detail_prev_hide()
        
        
    def on_detail_prev_show(self):
        self._show_detail = True
        
    def on_detail_prev_hide(self):
        self._show_detail = False
        
    def on_frame(self):
        ret, frame = self.cam.read()
        if ret:
            self.vis = frame.copy()
            if self._show_detail:
                vis_small = self._downscale_2(self.vis)
            else:
                vis_small = self._downscale_4(self.vis)
            
            if self._frame_count % 15 == 0:
                self.meta_img = MetaImg(vis_small, {})
                self.calib_filter(self.meta_img)
                self.sep_filter(self.meta_img)
                self._frame_count = 0
            meta = self.meta_img.meta
            if meta.get('ellipsis', None) is not None:
                print('w', meta['ellipsis'][1][0] * meta['mm_on_px'],
                      'h', meta['ellipsis'][1][1] * meta['mm_on_px'])
                cv2.ellipse(vis_small, meta['ellipsis'], (0,255,0))
            
            if meta.get('red_dot_ellipsis', None) is not None:
                cv2.ellipse(vis_small, meta['red_dot_ellipsis'], (0,0,255))
            
            if meta.get('mask', None) is not None:
                mask = meta['mask']
                shape = mask.shape[0], mask.shape[1], 3
                mask3 = np.zeros(shape, dtype=np.uint8)
                mask3[:,:,0] = mask
                if mask3.shape == vis_small.shape:
                    vis_small = cv2.addWeighted(vis_small, 1.0, mask3, 0.3, 0)
            
            self.video_widget.push_frame(vis_small)
            self._frame_count += 1
        else:
            self._reset_cam(self._prev_grab_res)
             
             
    def start(self):
        assert(self.video_widget)
        assert(self.form)
        self._reset_cam(self._prev_grab_res)
        self._timer.start(50)
        
    def _reset_cam(self, res):
        w, h = res
        self.cam = cv2.VideoCapture(self.cam_num)
        self.cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, w)
        self.cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, h)
        
    def _stop_cam(self):
        self.cam.release()
        
    def _change_res_cam(self, res):
        w, h = res
        self.cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, w)
        self.cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, h)
   
    def _downscale_4(self, img):
        h, w, d = img.shape
        img2 = np.zeros((h >> 2, w >> 2, d), dtype=np.uint8)
        for i in xrange(0, h, 4):
            for j in xrange(0, w, 4):
                img2[i >> 2][j >> 2] = img[i][j]
        return img2
    
    def _downscale_2(self, img):
        h, w, d = img.shape
        img2 = np.zeros((h >> 1, w >> 1, d), dtype=np.uint8)
        for i in xrange(0, h, 2):
            for j in xrange(0, w, 2):
                img2[i >> 1][j >> 1] = img[i][j]
        return img2
     
if __name__ == '__main__':
    app = App(sys.argv)
    form = MainWindow()
    app.set_form(form)
    app.set_video_widget(form.video_widget)
    app.start()
    form.show()
    sys.exit(app.exec_())
