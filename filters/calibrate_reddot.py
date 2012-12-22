from base_filter import BaseFilter
import cv2.cv as cv
import cv2
import numpy as np
import math

class CalibrateRedDotFilter(BaseFilter):
    
    def __init__(self, params={}):
        p = {'dims': (5,5),
             'dot_diameter_in_mm': 1}
        p.update(params)
        
        super(CalibrateRedDotFilter, self).__init__(p)
    
    def filter(self, meta_img):
        red = self._red_filter(meta_img.img)
        contour = self._find_max_contour(red)
        if len(contour) > 5:
            ellipsis = cv2.fitEllipse(contour.astype('int'))
            meta_img.meta['red_dot_contour'] = contour
            meta_img.meta['red_dot_ellipsis'] = ellipsis
            avg_diameter = self._avg_diameter(ellipsis)
            meta_img.meta['mm_on_px'] = self.params['dot_diameter_in_mm'] / avg_diameter
            meta_img.meta['ok'] = meta_img.meta.get('ok', True)
        else:
            meta_img.meta['red_dot'] = None
            meta_img.meta.get('errors', []).append('No chessboard!')
            meta_img.meta['mm_on_px'] = 5.0
            meta_img.meta['ok'] = False

    def _red_filter(self, img):
        r = img[:,:,2].astype(np.int32)
        g = img[:,:,1].astype(np.int32)
        b = img[:,:,1].astype(np.int32)
        ret = 100*r - 79*g - 79*b
        ret /= 100
        ret.clip(0, 255, out=ret)
        ret = ret.astype(np.uint8)
        _, ret = cv2.threshold(ret, 30, 255, type=cv2.THRESH_BINARY)
        return ret
    
    def _find_max_contour(self, mask):
        contours, _ = cv2.findContours(np.array(mask), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        try:
            area, i = max([(cv2.contourArea(contour.astype('int')), i) for i, contour in enumerate(contours)])
        except ValueError: #no  contours
            return []
        contour = contours[i]
        return contour
    
    def _avg_diameter(self, ellipsis):
        return (ellipsis[1][0] + ellipsis[1][1]) / 2
    
    