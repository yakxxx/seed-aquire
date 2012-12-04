import unittest
from filters.base_filter import BaseFilter, MetaImg
from filters.calibrate_chessboard import CalibrateChessFilter
from filters.separate_object import SeparateObjectFilter
import cv2.cv as cv
import cv2
import numpy as np


class CalibrationFilterTest(unittest.TestCase):
    
    def setUp(self):
        self.lena3_ref = cv2.imread('tests/lena.jpg', cv2.CV_LOAD_IMAGE_COLOR);
        self.lena3 = cv2.imread('tests/lena.jpg', cv2.CV_LOAD_IMAGE_COLOR)
        
        self.chess_and_oval1 = cv2.imread('tests/chess_and_oval1.jpg', cv.CV_LOAD_IMAGE_COLOR)
        
    def test_empty_filter(self):
        class EmptyFilter(BaseFilter):
            def filter(self, meta_img):
                return meta_img
            
        f1 = EmptyFilter()
        meta_img  = MetaImg('asd',{})
        f1(meta_img)
        self.assertEqual(meta_img.img, 'asd')
        
    def test_gray(self):
        f1 = CalibrateChessFilter()
        meta_img = MetaImg(self.lena3, {})
        f1(meta_img)
        self.assertEqual(meta_img.meta['gray'].shape[:2], self.lena3_ref.shape[:2])
     
    def test_avg(self):
        f1 = CalibrateChessFilter({'dims':(3,2)})
        avg = f1._avg_square_size_in_px(np.array( [ [[3.0,1.0]], [[4.0,1.0]], [[5.0, 1.0]], \
                                       [[3.0,2.0]], [[4.0,2.0]], [[5.0, 2.0]] ]))
        
        self.assertAlmostEqual(avg, 1.0)
        
    def find_corners_test(self):
        f1 = CalibrateChessFilter({'dims': (4,4),
                                   'square_size_in_mm': 5})
        meta_img = MetaImg(self.chess_and_oval1, {})
        f1(meta_img)
        self.assertLess(abs(meta_img.meta['mm_on_px'] - 0.3333), 0.05)
        
    def test_find_corners_tilted(self):
        im3 = cv2.imread('tests/chess3.jpg', cv2.CV_LOAD_IMAGE_COLOR)
        f1 = CalibrateChessFilter({'dims': (4,4),
                                   'square_size_in_mm': 5})
        meta_img = MetaImg(im3, {})
        f1(meta_img)
        self.assertTrue(meta_img.meta['ok'])
        
        
    def test_find_corners_real(self):
        im3 = cv2.imread('tests/chess5.jpg', cv2.CV_LOAD_IMAGE_COLOR)
        f1 = CalibrateChessFilter({'dims': (4,4),
                                   'square_size_in_mm': 5})
        meta_img = MetaImg(im3, {})
        f1(meta_img)
        self.assertTrue(meta_img.meta['ok'])
        
    
#    
#class SeparateObjectFilterTest(unittest.TestCase):
#    def setUp(self):
#        pass
#
#    def test_basic(self):
#        im3 = cv2.imread('tests/chess3.jpg', cv.CV_LOAD_IMAGE_COLOR)
#        f1 = SeparateObjectFilter()
#        meta_img = MetaImg(im3, {})
#        f1.filter(meta_img)
        
        
        
        
        