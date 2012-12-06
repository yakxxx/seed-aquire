from base_filter import BaseFilter
import cv2.cv as cv
import cv2
import numpy as np

class SeparateObjectFilter(BaseFilter):
    BG_PROBE_WIDTH = .08
    OBJECT_PROBE_WIDTH = 0.5
    
    def __init__(self, params={}):
        super(SeparateObjectFilter, self).__init__(params)
        
    def filter(self, meta_img):
        meta, mask = self._remove_bg(meta_img)
        meta_img.meta.update(meta)
        
        p1, p2, mask2 = self._remove_checkerboard(meta_img)
        cv2.rectangle(meta_img.img, p1, p2, (0,255,0))
        
        mask = np.bitwise_and(mask, mask2)
        meta_img.meta['mask'] = mask
        
        contour = self._find_max_contour(mask)
        if len(contour) > 5:
            ellipse = cv2.fitEllipse(contour.astype('int'))
            cv2.ellipse(meta_img.img, ellipse, (0,255,0))
            meta_img.meta['ellipse'] = ellipse
    

    def _remove_bg(self, meta_img):
        meta = {}
        mask = self._create_bg_probe_mask(meta_img.img)
        cut = np.ma.masked_array(meta_img.gray, mask)
        
        avg_bg = np.average(cut)
        std_bg = np.std(cut)
        meta['bg_avg'] = avg_bg
        meta['bg_std'] = std_bg
        thresh = avg_bg - 1.5*std_bg
        meta['bg_thresh'] = thresh
        _, mask = cv2.threshold(meta_img.gray, thresh, 255, type=cv2.THRESH_BINARY_INV)
        return meta, mask
    
    def _create_bg_probe_mask(self, img):
        size = img.shape[:2]
        w = int(round(self.BG_PROBE_WIDTH * max(20,min(size)))) 
        mask =  np.zeros(size, dtype=np.uint8)
        cv2.rectangle(mask, (0, 0), (w, w), 255, thickness=cv.CV_FILLED)
        cv2.rectangle(mask, (0, size[0]), (w, size[0] - w), 255, thickness=cv.CV_FILLED)
        cv2.rectangle(mask, (size[1], 0), (size[1] - w, w), 255, thickness=cv.CV_FILLED)
        cv2.rectangle(mask, (size[1], size[0]), (size[1] - w, size[0] - w), 255, thickness=cv.CV_FILLED)
        return mask
    
    def _remove_checkerboard(self, meta_img):
        found_all, corners = meta_img.corners
        if not found_all:
            size = meta_img.img.shape[:2]
            mask = np.empty(size, dtype=np.uint8)
            mask.fill(255)
            p1 = p2 = (0,0)
        else:
            x_cords = corners[:, 0, 0]
            y_cords = corners[:, 0, 1]
            center_x = np.average(x_cords)
            center_y = np.average(y_cords)
            width = int((max(x_cords) - min(x_cords)) * 1.65)
            height = int((max(y_cords) - min(y_cords)) * 1.65)
            
            size = meta_img.img.shape[:2]
            mask = np.empty(size, dtype=np.uint8)
            mask.fill(255)
            p1 = ( int(max(0, center_x - width/2)), int(max(0, center_y - width/2)) )
            p2 = ( int(min(size[0], center_x + width/2)), int(min(size[1], center_y + width/2)) )
            cv2.rectangle(mask, p1, p2, 
                    0, thickness=cv.CV_FILLED)
        
        return p1, p2, mask
        
    def _find_max_contour(self, mask):
        contours, _ = cv2.findContours(np.array(mask), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        try:
            area, i = max([(cv2.contourArea(contour.astype('int')), i) for i, contour in enumerate(contours)])
        except ValueError: #no  contours
            return []
        contour = contours[i]
        return contour
