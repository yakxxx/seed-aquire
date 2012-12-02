import unittest
from filters.base_filter import BaseFilter, MetaImg
from filters.calibrate_chessboard import CalibrateChessFilter
import cv2.cv as cv


class CalibrationFilterTest(unittest.TestCase):
    
    def setUp(self):
        self.lena3_ref = cv.LoadImage('tests/lena.jpg', cv.CV_LOAD_IMAGE_COLOR);
        self.lena3 = cv.LoadImage('tests/lena.jpg', cv.CV_LOAD_IMAGE_COLOR)
        
        self.chess_and_oval1 = cv.LoadImage('tests/chess_and_oval1.jpg', cv.CV_LOAD_IMAGE_COLOR)
        
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
        self.assertEqual(cv.GetSize(meta_img.meta['gray']), cv.GetSize(self.lena3_ref))
        self.assertEqual(meta_img.meta['gray'][0].type, cv.CV_8UC(1))
     
    def test_avg(self):
        f1 = CalibrateChessFilter({'dims':(3,2)})
        avg = f1._avg_square_size_in_px([(3.0,1.0), (4.0,1.0), (5.0, 1.0),
                                       (3.0,2.0), (4.0,2.0), (5.0, 2.0)])
        
        self.assertAlmostEqual(avg, 1.0)
        
    def find_corners_test(self):
        f1 = CalibrateChessFilter({'dims': (4,4),
                                   'square_size_in_mm': 5})
        meta_img = MetaImg(self.chess_and_oval1, {})
        f1(meta_img)
        self.assertLess(abs(meta_img.meta['mm_on_px'] - 0.3333), 0.05)