import unittest
from qt_app import *
import os, sys

class TestQtApp(unittest.TestCase):
    
    def setUp(self):
        CONFIG['save_folder'] = 'tests/tmp'
        
        if os.path.isdir('tests/tmp'):
            self._delete_dir('tests/tmp')
        os.mkdir('tests/tmp')

    def tearDown(self):
        self._delete_dir('tests/tmp')
    
    def test_app(self):
        app = App(sys.argv, conf = CONFIG)
        self.assertEqual(app._parse_last_measure_no(), 0)

        f = open('tests/tmp/measure.txt', 'w')
        f.write('123,label,w,h,img\n')
        f.close()
        self.assertEqual(app._parse_last_measure_no(), 123)        
        
        app._save_measure(126, 'xax', (1.2, 2.3), 'dupa.png')
        f = open('tests/tmp/measure.txt')
        for l in f:
            pass
        self.assertEqual(l, '126,xax,1.200,2.300,dupa.png\n')
        
    def _delete_dir(self, top):
        if top == '/':
            return
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(top)