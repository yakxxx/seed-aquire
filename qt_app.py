#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import cv2

from main_window import MainWindow
from filters import *
from video_thread import VideoThread
from save_dialog import SaveDialog
   
   
CONFIG = {
           'dot_diameter_in_mm': 1,
           'cam_num': 1,
           'save_folder': 'data',
           'measure_file': 'measure.txt'
          }

class App(QApplication):     
    def __init__(self, *args, **kwargs):
        self.conf = kwargs.pop('conf')
        super(App, self).__init__(*args, **kwargs)
        self.video_widget = None
        self.video_thread = None
        self.meta_img = None
        self.form = None

        
    def set_video_widget(self, video_widget, conf = {}):
        self.video_widget = video_widget
        self.video_thread = VideoThread(video_widget, conf)
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
        frame, downscaled = self.video_thread.snap()
        sizes = self._measure(downscaled)
        self._show_save_dialog(frame, downscaled, sizes)
        
    def _measure(self, img):
        meta_img = MetaImg(img, {})
        calib_filter = CalibrateRedDotFilter({'dot_diameter_in_mm': CONFIG.get('dot_diameter_in_mm', 1)})
        sep_filter = SeparateObjectFilter()
        calib_filter(meta_img)
        sep_filter(meta_img)
        w = meta_img.meta['ellipsis'][1][0] * meta_img.meta['mm_on_px']
        h = meta_img.meta['ellipsis'][1][1] * meta_img.meta['mm_on_px']
        return w,h
    
    def _show_save_dialog(self, frame, downscaled, sizes):
        self.save_dialog = QDialog()
        self.save_dialog.ui = SaveDialog(downscaled, sizes)
        self.save_dialog.ui.setupUi(self.save_dialog)
        self.save_dialog.show()
        self.save_dialog.accepted.connect(lambda: self._save_image_data(frame, sizes))
        
    def _save_image_data(self, frame, sizes):
        no = self._parse_last_measure_no()
        no += 1
        label = str(self.form.class_name.toPlainText())
        label = re.sub(r'[^\w]', '', label) or 'no_label'
        img_name = '%d_%s.png' % (no, label)
        path = self.conf.get('save_folder', './')
        path = os.path.join(path, img_name)
        cv2.imwrite(path, frame)
        
        self._save_measure(no, label, sizes, img_name)
        
    def _parse_last_measure_no(self):
        path = self.conf.get('save_folder', './')
        try:
            f = open(os.path.join(path, self.conf['measure_file']), 'r')
        except IOError:
            return 0
        
        for last_line in f:
            pass
        f.close()
        
        if last_line:
            return int(last_line.split(',')[0])
        else:
            return 0
        
    def _save_measure(self, no, label, sizes, img_name):
        path = self.conf.get('save_folder', './')
        f = open(os.path.join(path, self.conf['measure_file']), 'a+')
        f.write("%d,%s,%.3f,%.3f,%s\n" % (no, label, sizes[0], sizes[1], img_name))
        f.close()
        
                        
        
    def start(self):
        assert(self.video_widget)
        assert(self.form)
        self.video_thread.start()
   
     
if __name__ == '__main__':
    try:
        CONFIG['cam_num'] = int(sys.argv[1])
    except IndexError:
        print "No cam_num given using %d" % CONFIG['cam_num']

    if not os.path.isdir(CONFIG['save_folder']):
        os.mkdir(CONFIG['save_folder'])

    app = App(sys.argv, conf = CONFIG)
    form = MainWindow()
    app.set_form(form)
    app.set_video_widget(form.video_widget, CONFIG)
    app.start()
    form.show()
    sys.exit(app.exec_())
