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

from video_thread import VideoThread

   
class App(QApplication):     
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.video_widget = None
        self.video_thread = None
        self.meta_img = None
        self.form = None
        
    def set_video_widget(self, video_widget):
        self.video_widget = video_widget
        self.video_thread = VideoThread(video_widget)
        if self.form:
            self.video_thread.set_separation_threshold(self.form.threshold.value())
        
    def set_form(self, form):
        self.form = form
        self.form.key_press.connect(self.on_key_press)
        self.form.key_release.connect(self.on_key_release)
        self.form.destroyed.connect(self.on_exit)
        self.form.show_mask.stateChanged.connect(self.on_show_mask)
        self.form.threshold.valueChanged.connect(self.on_thresh_change)
        if self.video_thread:
            self.video_thread.set_separation_threshold(self.form.threshold.value())
        
    def on_key_press(self, key):
        if key and key == Qt.Key_Alt:
            self.on_detail_prev_show()
        elif key and key == Qt.Key_Control:
            self.on_snap()
        
    def on_key_release(self, key):
        if key and key == Qt.Key_Alt:
            self.on_detail_prev_hide()
            
    def on_exit(self):
        self.video_thread.kill()
        
    def on_show_mask(self, state):
        if state == Qt.Checked:
            self.video_thread.show_mask()
        else:
            self.video_thread.hide_mask()
            
    def on_thresh_change(self, value):
        self.video_thread.set_separation_threshold(value)
        
    def on_detail_prev_show(self):
        self.video_thread.show_detail()
        
    def on_detail_prev_hide(self):
        self.video_thread.hide_detail()
        
    def on_snap(self):
        self.video_thread.snap()
        
    def start(self):
        assert(self.video_widget)
        assert(self.form)
        self.video_thread.start()
   
     
if __name__ == '__main__':
    app = App(sys.argv)
    form = MainWindow()
    app.set_form(form)
    app.set_video_widget(form.video_widget)
    app.start()
    form.show()
    sys.exit(app.exec_())
