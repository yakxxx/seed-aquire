from base_filter import BaseFilter
import cv2.cv as cv
import cv2
import numpy as np

class SeparateObjectFilter(BaseFilter):
    BG_PROBE_WIDTH = 50
    
    
    def __init__(self, params={}):
        super(SeparateObjectFilter, self).__init__(params)
        
    def filter(self, meta_img):
       self._create_bg_probe_mask(meta_img.img)
    
    
    
    def _create_bg_probe_mask(self, img):
        w = self.BG_PROBE_WIDTH
        size = cv.GetSize(img)
        mask =  np.zeros(size, 8, 1)
        cv.Zero(mask)
        cv2.rectangle(mask, (0, 0), (w, w), 255, thickness=cv.CV_FILLED)
        cv2.rectangle(mask, (size[0], 0), (size[0] - w, w), 255, thickness=cv.CV_FILLED)
        cv2.rectangle(mask, (0, size[1]), (w, size[1] - w), 255, thickness=cv.CV_FILLED)
        cv2.rectangle(mask, (size[0], size[1]), (size[0] - w, size[1] - w), 255, thickness=cv.CV_FILLED)
        cv2.threshold(mask, mask, 127.0, 255)

        
        cv.ShowImage('win', mask)
        cv.WaitKey()
        cv.DestroyAllWindows()