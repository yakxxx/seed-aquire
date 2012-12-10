#!/usr/bin/python
# -*- coding: utf-8 -*-
    
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from main_window import MainWindow
   
   
   
#class Form(QDialog, MainWindow):
#    
#    def __init__(self, parent=None):
#        super(Form, self).__init__(parent)
#        super(Form, self).setupUi(parent)
#
#    def greetings(self):
#        print ("Hello %s" % self.edit.text())        
     
     
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = MainWindow()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
