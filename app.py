import cv2
import cv2.cv as cv
import numpy as np
from filters.calibrate_chessboard import CalibrateChessFilter
from filters.separate_object import SeparateObjectFilter
from filters.base_filter import MetaImg


class App(object):
    def __init__(self, video_src = 0):
        self.cam = cap = cv2.VideoCapture(video_src)
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 200)
        ret, self.frame = self.cam.read()
        cv2.namedWindow('win')
        self.calib_filter = CalibrateChessFilter({'dims': (4,4),
                                   'square_size_in_mm': 5})
        self.sep_filter = SeparateObjectFilter()
        
    def run(self):
        while True:
            ret, self.frame = self.cam.read()
            vis = self.frame.copy()
            meta_img = MetaImg(vis, {})
            self.calib_filter(meta_img)
            self.sep_filter(meta_img)
            cv2.imshow('win', meta_img.img)
            
            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            
        cv2.destroyAllWindows()
            
a = App()
a.run()