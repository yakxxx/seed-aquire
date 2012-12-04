from base_filter import BaseFilter
import cv2.cv as cv

class SeparateObjectFilter(BaseFilter):
    
    def __init__(self, params={}):
        p = {'dims': (4,4),
             'square_size_in_mm': 5}
        p.update(params)
        
        super(SeparateObjectFilter, self).__init__(p)
    