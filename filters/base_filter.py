# -*- coding: utf-8 -*-
import cv2.cv as cv
import cv2


class MetaImg(object):
    def __init__(self, img, meta, params={'dims': (4,4)}):
        self.img = img
        self.meta = meta
        self.params = params
        self._gray = None
        
    @property
    def gray(self):
        if self._gray != None:
            return self._gray
        
        self._gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        return self.gray
    

class BaseFilter(object):
    def __init__(self, params = {}):
        self.params = params
        
    def filter(self, meta_img):
        raise NotImplementedError()
    
    def __call__(self, meta_img):
        assert(isinstance(meta_img, MetaImg))
        return self.filter(meta_img)