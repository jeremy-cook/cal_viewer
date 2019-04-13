# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CalViewer.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(573, 342)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("MainWindow {background-color:black;}")
        self.verticalLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 571, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.SectionSelect = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.SectionSelect.setMinimumSize(QtCore.QSize(200, 0))
        self.SectionSelect.setObjectName("SectionSelect")
        self.horizontalLayout.addWidget(self.SectionSelect)
        navBarSpacer = QtWidgets.QnavBarSpacer(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(navBarSpacer)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.splitter = QtWidgets.QSplitter(self.verticalLayoutWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.treeWidget_2 = QtWidgets.QTreeWidget(self.splitter)
        self.treeWidget_2.setObjectName("treeWidget_2")
        self.treeWidget_2.headerItem().setText(0, "Calibrations")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.splitter)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.verticalLayout.addWidget(self.splitter)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CalViewer"))
        MainWindow.setAccessibleName(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "CalViewer"))

