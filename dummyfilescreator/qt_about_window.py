# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/qt/About.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class UiAbout(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(182, 101)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(About.sizePolicy().hasHeightForWidth())
        About.setSizePolicy(sizePolicy)
        About.setMinimumSize(QtCore.QSize(182, 101))
        About.setMaximumSize(QtCore.QSize(182, 101))
        self.label = QtWidgets.QLabel(About)
        self.label.setGeometry(QtCore.QRect(10, 10, 161, 81))
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "About"))
        self.label.setText(
            _translate(
                "About",
                '<html><head/><body><p align="center">2022 <a href="https://github.com/matuzalemmuller/dummy-files-creator"><span style=" text-decoration: underline; color:#0000ff;">Dummy Files Creator</span></a></p><p align="center">by <a href="https://matuzalemmuller.com"><span style=" text-decoration: underline; color:#0000ff;">Matuzalem (Mat) Muller</span></a></p><p align="center">v3.0.0</p></body></html>',
            )
        )
