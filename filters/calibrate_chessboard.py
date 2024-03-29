from base_filter import BaseFilter
import cv2.cv as cv
import cv2
import numpy as np
import math

class CalibrateChessFilter(BaseFilter):
    
    def __init__(self, params={}):
        p = {'dims': (5,5),
             'square_size_in_mm': 5}
        p.update(params)
        
        super(CalibrateChessFilter, self).__init__(p)
    
    def filter(self, meta_img):
        found_all, corners = meta_img.corners
        if not found_all:
            meta_img.meta.get('errors', []).append('No chessboard!')
            meta_img.meta['mm_on_px'] = 5
            meta_img.meta['ok'] = False
        else:
            avg_ss_px = self._avg_square_size_in_px(corners)
            meta_img.meta['mm_on_px'] = self.params['square_size_in_mm'] / avg_ss_px
            meta_img.meta['ok'] = meta_img.meta.get('ok', True)
            cv2.drawChessboardCorners(meta_img.img, self.params['dims'], corners, found_all)
            
    
    def _avg_square_size_in_px(self, corners):
        tmp_sum = 0
        for i, corner in enumerate(corners):
            if i % self.params['dims'][0] == self.params['dims'][0] - 1:
                continue
            tmp_sum += self._dist(corners[i][0], corners[i+1][0])
        return tmp_sum / ((self.params['dims'][0] - 1) * self.params['dims'][1])
                
    def _dist(self, p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2) 
            