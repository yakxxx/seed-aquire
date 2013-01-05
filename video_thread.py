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
from threading import *
import time


class VideoThread(Thread):
    
    def __init__(self, video_widget, conf):
        super(VideoThread, self).__init__()
        self.cam_num = conf.get('cam_num', 0)
        self.red_dot_diameter = conf.get('dot_diameter_in_mm', 1)
        self._frame_count = 0
        self._show_detail = False
        self._killed = False
        self._show_mask = False
        self._prev_grab_res = (1280, 1024)
        self._snap_grab_res = (2592, 1944)
        self.video_widget = video_widget
        self._cam_mutex = Lock()
        
        self.calib_filter = CalibrateRedDotFilter({'dot_diameter_in_mm': self.red_dot_diameter})
        self.sep_filter = SeparateObjectFilter()
        
        self._timer = QTimer()
        self._timer.timeout.connect(self.on_frame)
        
    def run(self, delay=50):
        while not self._killed:
            time.sleep(0.05)
            self.on_frame()
        
    def start(self, *args, **kwargs):
        self._reset_cam(self._prev_grab_res)
        return super(VideoThread, self).start(*args, **kwargs)
    
    def kill(self):
        self._killed = True
    
    def show_detail(self):
        self._show_detail = True
        
    def hide_detail(self):
        self._show_detail = False
        
    def show_mask(self):
        self._show_mask = True
        
    def hide_mask(self):
        self._show_mask = False
        
    def set_separation_threshold(self, value):
        self.sep_filter.set_thresh(value)
        
    def snap(self):
        self._change_res_cam(self._snap_grab_res)
        ret, frame = self.read_cam()
#        if ret:
#            cv2.imshow('snapshot', self._downscale_4(frame))
        self._change_res_cam(self._prev_grab_res)
        downscaled = self._downscale_4(frame)
        return frame, downscaled
    
    def on_frame(self):
        ret, frame = self.read_cam()
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
            self._add_overlays(meta, vis_small)
            self.video_widget.push_frame(vis_small)
            self._frame_count += 1
        else:
            self._reset_cam(self._prev_grab_res)
            
    def read_cam(self):
        self._cam_mutex.acquire()
        ret = self.cam.read()
        self._cam_mutex.release()
        return ret
    
    def _reset_cam(self, res):
        w, h = res
        self._cam_mutex.acquire()
        self.cam = cv2.VideoCapture(self.cam_num)
        self.cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, w)
        self.cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, h)
        self._cam_mutex.release()
        
    def _stop_cam(self):
        self._cam_mutex.acquire()
        self.cam.release()
        self._cam_mutex.release()
        
    def _change_res_cam(self, res):
        w, h = res
        self._cam_mutex.acquire()
        self.cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, w)
        self.cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, h)
        self._cam_mutex.release()
   
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
    
    def _add_overlays(self, meta, img):
        if meta.get('ellipsis', None) is not None:
            print('w', meta['ellipsis'][1][0] * meta['mm_on_px'],
                  'h', meta['ellipsis'][1][1] * meta['mm_on_px'])
            cv2.ellipse(img, meta['ellipsis'], (0, 255, 0))
            
        if meta.get('red_dot_ellipsis', None) is not None:
            cv2.ellipse(img, meta['red_dot_ellipsis'], (0, 0, 255))
            
        if meta.get('mask', None) is not None and self._show_mask:
            mask = meta['mask']
            shape = mask.shape[0], mask.shape[1], 3
            mask3 = np.zeros(shape, dtype=np.uint8)
            mask3[:, :, 0] = mask
            if mask3.shape == img.shape:
                cv2.addWeighted(img, 1.0, mask3, 0.3, 0, img)
                
                
                