from base_filter import BaseFilter
import cv2.cv as cv
import cv2
import math

class CalibrateChessFilter(BaseFilter):
    
    def __init__(self, params={}):
        p = {'dims': (4,4),
             'square_size_in_mm': 5}
        p.update(params)
        
        super(CalibrateChessFilter, self).__init__(p)
    
    def filter(self, meta_img):
        gray = self._to_gray(meta_img.img) 
        meta_img.meta['gray'] = gray
        found_all, corners = self._find_corners(gray)
        if not found_all:
            meta_img.meta.get('errors', []).append('No chessboard!')
            meta_img.meta['mm_on_px'] = 5
        else:
            avg_ss_px = self._avg_square_size_in_px(corners)
            meta_img.meta['mm_on_px'] = self.params['square_size_in_mm'] / avg_ss_px
            cv.DrawChessboardCorners(meta_img.img, self.params['dims'], corners, found_all)
            
                          
    def _to_gray(self, img):
        gray =  cv.CreateImage(cv.GetSize(img), 8, 1)
        cv.CvtColor(img, gray, cv.CV_RGB2GRAY)
        return gray
    
    def _find_corners(self, gray):
        return cv.FindChessboardCorners(gray, self.params['dims'], flags=cv.CV_CALIB_CB_ADAPTIVE_THRESH + cv.CV_CALIB_CB_NORMALIZE_IMAGE)
    
    def _avg_square_size_in_px(self, corners):
        tmp_sum = 0
        for i, corner in enumerate(corners):
            if i % self.params['dims'][0] == self.params['dims'][0] - 1:
                continue
            tmp_sum += self._dist(corners[i], corners[i+1])
        return tmp_sum / ((self.params['dims'][0] - 1) * self.params['dims'][1])
                
    def _dist(self, p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2) 
            