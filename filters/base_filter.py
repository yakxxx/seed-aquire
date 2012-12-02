from collections import namedtuple


MetaImg = namedtuple('MetaImg', ['img', 'meta'])


class BaseFilter(object):
    
    def __init__(self, params = {}):
        self.params = params
        
    def filter(self, meta_img):
        raise NotImplementedError()
    
    def __call__(self, meta_img):
        assert(isinstance(meta_img, MetaImg))
        return self.filter(meta_img)