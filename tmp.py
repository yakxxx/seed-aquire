# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_app.ui'
#
# Created: Sun Dec 23 17:33:22 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(self.centralWidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.video_widget = QtGui.Qvideo_widget(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_widget.sizePolicy().hasHeightForWidth())
        self.video_widget.setSizePolicy(sizePolicy)
        self.video_widget.setMinimumSize(QtCore.QSize(640, 480))
        self.video_widget.setBaseSize(QtCore.QSize(0, 0))
        self.video_widget.setObjectName(_fromUtf8("video_widget"))
        self.verticalLayout.addWidget(self.video_widget)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_2.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox_2.setBaseSize(QtCore.QSize(0, 0))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.class_name = QtGui.QTextEdit(self.groupBox_2)
        self.class_name.setGeometry(QtCore.QRect(10, 50, 161, 21))
        self.class_name.setObjectName(_fromUtf8("class_name"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(10, 30, 81, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.show_mask = QtGui.QCheckBox(self.groupBox_2)
        self.show_mask.setGeometry(QtCore.QRect(10, 90, 101, 21))
        self.show_mask.setObjectName(_fromUtf8("show_mask"))
        self.threshold = QtGui.QSpinBox(self.groupBox_2)
        self.threshold.setGeometry(QtCore.QRect(10, 130, 52, 28))
        self.threshold.setMaximum(400)
        self.threshold.setProperty("value", 80)
        self.threshold.setObjectName(_fromUtf8("threshold"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(70, 130, 91, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.snap_button = QtGui.QPushButton(self.centralWidget)
        self.snap_button.setObjectName(_fromUtf8("snap_button"))
        self.gridLayout.addWidget(self.snap_button, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.mainToolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Class name", None, QtGui.QApplication.UnicodeUTF8))
        self.show_mask.setText(QtGui.QApplication.translate("MainWindow", "Show Mask", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Threshold", None, QtGui.QApplication.UnicodeUTF8))
        self.snap_button.setText(QtGui.QApplication.translate("MainWindow", "Snap", None, QtGui.QApplication.UnicodeUTF8))

