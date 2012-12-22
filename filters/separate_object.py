from base_filter import BaseFilter
import cv2.cv as cv
import cv2
import numpy as np
import math

class SeparateObjectFilter(BaseFilter):
    BG_PROBE_WIDTH = .06
    OBJECT_PROBE_WIDTH = 0.5
    THRESH_BAR = 0.8 #threshold = avg_bg - THRESH_BAR * std_bg
    
    def __init__(self, params={}):
        super(SeparateObjectFilter, self).__init__(params)
        
    def filter(self, meta_img):
        mask = self._remove_bg(meta_img)
        
        p1, p2, mask2 = self._remove_red_dot(meta_img)
        
        mask = np.bitwise_and(mask, mask2)
        meta_img.meta['mask'] = mask
        
        contour = self._find_max_contour(mask)
        if len(contour) > 5:
            ellipse = cv2.fitEllipse(contour.astype('int'))
            meta_img.meta['ellipsis'] = ellipse
    

    def _remove_bg(self, meta_img):
        mask = self._create_bg_probe_mask(meta_img.img)
        hsv = cv2.cvtColor(meta_img.img, cv.CV_BGR2HSV)
        probab = self._bg_probability(mask, hsv[:,:,1])
        probab += 0.2 * self._bg_probability(mask, hsv[:,:,2])
        probab *= 10000
        probab = np.clip(probab, 0, 255)
        probab = probab.astype(np.uint8) 
        _, mask = cv2.threshold(probab, 80 , 255, type=cv2.THRESH_BINARY_INV)
        return mask
    
    def _create_bg_probe_mask(self, img):
        size = img.shape[:2]
        w = int(round(self.BG_PROBE_WIDTH * max(20,min(size)))) 
        mask =  np.zeros(size, dtype=np.uint8)
        cv2.rectangle(mask, (0, 0), (w, w), 255, thickness=cv.CV_FILLED)
        cv2.rectangle(mask, (0, size[0]), (w, size[0] - w), 255, thickness=cv.CV_FILLED)
        cv2.rectangle(mask, (size[1], 0), (size[1] - w, w), 255, thickness=cv.CV_FILLED)
        cv2.rectangle(mask, (size[1], size[0]), (size[1] - w, size[0] - w), 255, thickness=cv.CV_FILLED)
        return mask
    
    def _bg_probability(self, bg_probe_mask, layer):
        cut = np.ma.masked_array(layer, bg_probe_mask)
        avg_bg = np.average(cut)
        std_bg = np.std(cut)
        ret = np.zeros(cut.shape)
        probab = np.vectorize(lambda px: self._normpdf(px, avg_bg, std_bg))
        ret = probab(layer)
        return ret
    
    def _remove_red_dot(self, meta_img):
        red_dot_cont = meta_img.meta.get('red_dot_contour', False)
        if red_dot_cont is not False:
            x_cords = red_dot_cont[:, 0, 0]
            y_cords = red_dot_cont[:, 0, 1]
            center_x = (np.max(x_cords) + np.min(x_cords)) / 2
            center_y = (np.max(y_cords) + np.min(y_cords)) / 2
            width = int((max(x_cords) - min(x_cords)) * 1.15)
            height = int((max(y_cords) - min(y_cords)) * 1.15)
            
            size = meta_img.img.shape[:2]
            mask = np.empty(size, dtype=np.uint8)
            mask.fill(255)
            p1 = ( int(max(0, center_x - width/2)), int(max(0, center_y - height/2)) )
            p2 = ( int(min(size[1], center_x + width/2)), int(min(size[0], center_y + height/2)) )
            cv2.rectangle(mask, p1, p2, 
                    0, thickness=cv.CV_FILLED)
        else:
            size = meta_img.img.shape[:2]
            mask = np.empty(size, dtype=np.uint8)
            mask.fill(255)
            p1 = p2 = (0,0)
            
        return p1, p2, mask
        
    def _find_max_contour(self, mask):
        contours, _ = cv2.findContours(np.array(mask), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        try:
            area, i = max([(cv2.contourArea(contour.astype('int')), i) for i, contour in enumerate(contours)])
        except ValueError: #no  contours
            return []
        contour = contours[i]
        return contour
    
    def _normpdf(self,x, mean, sd):
        if sd == 0:
            return 1.0
        var = float(sd)**2
        pi = 3.1415926
        denom = (2*pi*var)**.5
        num = math.exp(-(float(x)-float(mean))**2/(2*var))
        return num/denom
