import unittest
from filters.base_filter import BaseFilter, MetaImg
from filters.separate_object import SeparateObjectFilter
from filters.calibrate_reddot import CalibrateRedDotFilter
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
        f1 = CalibrateRedDotFilter()
        meta_img = MetaImg(self.lena3, {})
        f1(meta_img)
        self.assertEqual(meta_img.gray.shape[:2], self.lena3_ref.shape[:2])
     
    def test_avg(self):
        f1 = CalibrateRedDotFilter({'dims':(3,2)})
        avg = f1._avg_diameter(((10,10),(20,30),78))
        
        self.assertAlmostEqual(avg, 25)
        
    def test_chess_speed(self):
        im3 = cv2.imread('tests/reddot_seed.jpg', cv2.CV_LOAD_IMAGE_COLOR)
        f1 = CalibrateRedDotFilter({'dims': (4,4),
                                   'dot_diameter_in_mm': 5})
        t = time()
        for i in xrange(25):
            meta_img = MetaImg(np.array(im3), {})
            f1.filter(meta_img)
        t2 = time()
        self.assertLess(t2-t, 4)
        
        
class RedDotCalibrationTest(unittest.TestCase):
    
    def test_red_filter(self):
        im3 = cv2.imread('tests/reddot_seed.jpg', cv2.CV_LOAD_IMAGE_COLOR)
        f = CalibrateRedDotFilter()
        imred = f._red_filter(im3)
        self.assertGreater(np.sum(imred), 400)
        
    def test_filter(self):
        im3 = cv2.imread('tests/reddot_seed.jpg', cv2.CV_LOAD_IMAGE_COLOR)
        f = CalibrateRedDotFilter()
        meta_img = MetaImg(im3, {})
        f(meta_img)
        self.assertTrue(meta_img.meta['ok'])
        self.assertAlmostEqual(meta_img.meta['mm_on_px'], 0.010925770496)
        
class SeparateObjectFilterTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_bg_avg(self):
        im3 = cv2.imread('tests/reddot_seed.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = SeparateObjectFilter()
        meta_img = MetaImg(im3, {})
        f1.filter(meta_img)
        cv2.imwrite('mask.png', meta_img.meta['mask'])
        self.assertGreater(meta_img.meta['bg_avg'], 160)
        
    def test_remove_reddot(self):
        im3 = cv2.imread('tests/reddot.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f0 = CalibrateRedDotFilter()
        f1 = SeparateObjectFilter()
        meta_img = MetaImg(im3, {})
        f0.filter(meta_img)
        f1.filter(meta_img)
        self.assertLess(np.sum(meta_img.meta['mask'])/255, 30)
        
    def test_elipse(self):
        im3 = cv2.imread('tests/reddot_seed.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = SeparateObjectFilter()
        meta_img = MetaImg(im3, {})
        f1.filter(meta_img)
        self.assertTrue(meta_img.meta.get('ellipsis', False))
        
    def test_no_red_dot(self):
        im3 = cv2.imread('tests/lena.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = SeparateObjectFilter()
        meta_img = MetaImg(im3, {})
        try:
            f1.filter(meta_img)
        except:
            self.fail()
            
    def test_no_object(self):
        im3 = cv2.imread('tests/no_object.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = SeparateObjectFilter()
        meta_img = MetaImg(im3, {})
        try:
            f1.filter(meta_img)
        except:
            self.fail()
            
    def test_speed(self):
        im3 = cv2.imread('tests/reddot_seed.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = SeparateObjectFilter()
        t = time()
        for i in xrange(25):
            meta_img = MetaImg(im3, {})
            f1.filter(meta_img)
        t2 = time()
        self.assertLess(t2-t, 5) #at least 5 frames for second
#        cv2.imshow('win', meta_img.img)
#        cv2.waitKey()


    def test_measure(self):
        im3 = cv2.imread('tests/reddot_seed.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = CalibrateRedDotFilter({'dims': (4,4),
                                   'dot_diameter_in_mm': 5})
        f2 = SeparateObjectFilter()

        meta_img = MetaImg(im3, {})
        f1(meta_img)
        f2(meta_img)
        print meta_img.meta['ellipsis']
        

class SppedTest(unittest.TestCase):
    
    def full_fitlers_test(self):
        im3 = cv2.imread('tests/reddot_seed.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = CalibrateRedDotFilter({'dims': (4,4),
                                   'dot_diameter_in_mm': 5})
        f2 = SeparateObjectFilter()
        
        t = time()
        for i in xrange(25):
            meta_img = MetaImg(np.array(im3), {})
            f1.filter(meta_img)
            f2.filter(meta_img)
        t2 = time()
        self.assertLess(t2-t, 5) #at least 5 frames for second
    
        
        
        