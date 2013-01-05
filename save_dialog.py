# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'save_dialog.ui'
#
# Created: Sat Jan  5 13:10:08 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal as Signal
from video_widget import VideoWidget

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class SaveDialog(object):
    
    def __init__(self, frame, sizes):
        self._frame = frame
        self.w, self.h = sizes
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(733, 628)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(100, 570, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.video_widget = VideoWidget(Dialog)
        self.video_widget.setGeometry(QtCore.QRect(20, 20, 648, 486))
        self.video_widget.setObjectName("video_widget")
        self.video_widget.push_frame(self._frame)
        
        text = "W: %f<br />H: %f" % (self.w, self.h)
        self.measure_text = QtGui.QTextEdit(text, Dialog)
        self.measure_text.setGeometry(QtCore.QRect(540, 550, 151, 61))
        self.measure_text.setObjectName("measure_text")
        
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(540, 520, 55, 18))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(270, 540, 171, 21)) 
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Measure:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Is image quality acceptable?", None, QtGui.QApplication.UnicodeUTF8))

