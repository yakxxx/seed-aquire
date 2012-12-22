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
        self.assertLess(abs(meta_img.meta['mm_on_px'] - 0.0105), 0.005)
        
class SeparateObjectFilterTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_probe_mask(self):
        f = SeparateObjectFilter()
        im3 = cv2.imread('tests/reddot.jpg', cv.CV_LOAD_IMAGE_COLOR)
        mask = f._create_bg_probe_mask(im3)
        self.assertGreater(np.sum(mask)/255, 400)
        
    def test_remove_reddot(self):
        im3 = cv2.imread('tests/reddot.jpg', cv.CV_LOAD_IMAGE_COLOR)
        self._test_remove_reddot(im3)  
    
        im3 = cv2.imread('tests/reddot2.jpg', cv.CV_LOAD_IMAGE_COLOR)
        self._test_remove_reddot(im3)

        
    def _test_remove_reddot(self, img):
        
        f0 = CalibrateRedDotFilter()
        f1 = SeparateObjectFilter()
        meta_img = MetaImg(img, {})
        f0.filter(meta_img)
        f1.filter(meta_img)
        self.assertLess(np.sum(meta_img.meta['mask'])/255, 40)
        
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
#        try:
        f1.filter(meta_img)
#        except Exception as e:
#            print e
#            self.fail()
            
    def test_speed(self):
        im3 = cv2.imread('tests/reddot_seed.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = SeparateObjectFilter()
        t = time()
        for i in xrange(5):
            meta_img = MetaImg(im3, {})
            f1.filter(meta_img)
        t2 = time()
        self.assertLess(t2-t, 5) 

    @unittest.skip
    def test_bg_probability(self):
        im3 = cv2.imread('tests/reddot_seed.jpg', cv.CV_LOAD_IMAGE_COLOR)
        f1 = SeparateObjectFilter()
        meta_img = MetaImg(im3, {})
        hsv = cv2.cvtColor(meta_img.img, cv.CV_BGR2HSV)
        mask = f1._create_bg_probe_mask(im3)
        
        probab = f1._bg_probability(mask, hsv[:,:,2])
        _, ret = cv2.threshold((probab*10000).astype(np.uint8), 70 , 255, cv2.THRESH_BINARY_INV)
        cv2.imshow('asd1', ret)
        probab += f1._bg_probability(mask, hsv[:,:,0])
        
        probab *= 10000
        probab = probab.astype(np.uint8)
        print np.max(probab)
        _, ret = cv2.threshold(probab, 140 , 255, cv2.THRESH_BINARY_INV)


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
        for i in xrange(5):
            meta_img = MetaImg(np.array(im3), {})
            f1.filter(meta_img)
            f2.filter(meta_img)
        t2 = time()
        self.assertLess(t2-t, 5) #at least 2 frames for second
    
        
        
        