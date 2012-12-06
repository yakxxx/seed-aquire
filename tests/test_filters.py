import unittest
from filters.base_filter import BaseFilter, MetaImg
from filters.calibrate_chessboard import CalibrateChessFilter
from filters.separate_object import SeparateObjectFilter
import cv2.cv as cv
import cv2
import numpy as np
from time import time


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
        self.assertEqual(meta_img.gray.shape[:2], self.lena3_ref.shape[:2])
     
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
        
    def test_find_corners_joint(self):
        im3 = cv2.imread('tests/chess_and_seed2.jpg', cv2.CV_LOAD_IMAGE_COLOR)
        f1 = CalibrateChessFilter({'dims': (4,4),
                                   'square_size_in_mm': 5})
        meta_img = MetaImg(im3, {})
        f1(meta_img)
        self.assertTrue(meta_img.meta['ok'])
        
    def test_chess_speed(self):
        im3 = cv2.imread('tests/chess_and_seed2.jpg', cv2.CV_LOAD_IMAGE_COLOR)
        f1 = CalibrateChessFilter({'dims': (4,4),
                                   'square_size_in_mm': 5})
        t = time()
        for i in xrange(25):
            meta_img = MetaImg(np.array(im3), {})
            f1.filter(meta_img)
        t2 = time()
        self.assertLess(t2-t, 4)
        
        
        
class SeparateObjectFilterTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_bg_avg(self):
        im3 = cv2.imread('tests/chess_and_seed2.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = SeparateObjectFilter()
        meta_img = MetaImg(im3, {})
        f1.filter(meta_img)
        cv2.imwrite('mask.png', meta_img.meta['mask'])
        self.assertGreater(meta_img.meta['bg_avg'], 160)
        
    def test_remove_chessboard(self):
        im3 = cv2.imread('tests/chess3.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = SeparateObjectFilter()
        meta_img = MetaImg(im3, {})
        f1.filter(meta_img)
        self.assertLess(np.sum(meta_img.meta['mask'])/255, 30)
        
    def test_elipse(self):
        im3 = cv2.imread('tests/chess_and_seed2.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = SeparateObjectFilter()
        meta_img = MetaImg(im3, {})
        f1.filter(meta_img)
        self.assertTrue(meta_img.meta.get('ellipse', False))
        
        
    def test_speed(self):
        im3 = cv2.imread('tests/chess_and_seed2.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = SeparateObjectFilter()
        t = time()
        for i in xrange(25):
            meta_img = MetaImg(im3, {})
            f1.filter(meta_img)
        t2 = time()
        self.assertLess(t2-t, 5) #at least 5 frames for second
#        cv2.imshow('win', meta_img.img)
#        cv2.waitKey()


class SppedTest(unittest.TestCase):
    
    def full_fitlers_test(self):
        im3 = cv2.imread('tests/chess_and_seed2.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = CalibrateChessFilter({'dims': (4,4),
                                   'square_size_in_mm': 5})
        f2 = SeparateObjectFilter()
        
        t = time()
        for i in xrange(25):
            meta_img = MetaImg(np.array(im3), {})
            f1.filter(meta_img)
            f2.filter(meta_img)
        t2 = time()
        self.assertLess(t2-t, 5) #at least 5 frames for second
    
        
        
        