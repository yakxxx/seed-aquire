import cv2.cv as cv
import cv2



class MetaImg(object):
    
    def __init__(self, img, meta, params={'dims': (4,4)}):
        self.img = img
        self.meta = meta
        self.params = params
        self._gray = None
        self._corners = None
        
        
    @property
    def gray(self):
        if self._gray != None:
            return self._gray
        
        self._gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        return self.gray
    
    @property
    def corners(self):
        if self._corners != None:
            return self._corners
        
        found_all, corners = cv2.findChessboardCorners(self.gray,
                                    self.params['dims'],
                                    flags=cv2.CALIB_CB_NORMALIZE_IMAGE+ cv2.CALIB_CB_FILTER_QUADS + cv2.CALIB_CB_ADAPTIVE_THRESH)
        self._corners = found_all, corners
        return found_all, corners


class BaseFilter(object):
    
    def __init__(self, params = {}):
        self.params = params
        
    def filter(self, meta_img):
        raise NotImplementedError()
    
    def __call__(self, meta_img):
        assert(isinstance(meta_img, MetaImg))
        return self.filter(meta_img)