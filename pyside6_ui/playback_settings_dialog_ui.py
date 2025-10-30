# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'playback_settings_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QDoubleSpinBox, QGridLayout,
    QLabel, QSizePolicy, QWidget)

class Ui_playback_settings_dialog(object):
    def setupUi(self, playback_settings_dialog):
        if not playback_settings_dialog.objectName():
            playback_settings_dialog.setObjectName(u"playback_settings_dialog")
        playback_settings_dialog.resize(205, 48)
        self.gridLayoutWidget = QWidget(playback_settings_dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 10, 160, 23))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.speed_label = QLabel(self.gridLayoutWidget)
        self.speed_label.setObjectName(u"speed_label")

        self.gridLayout.addWidget(self.speed_label, 0, 0, 1, 1)

        self.speed_spinbox = QDoubleSpinBox(self.gridLayoutWidget)
        self.speed_spinbox.setObjectName(u"speed_spinbox")
        self.speed_spinbox.setMinimum(0.250000000000000)
        self.speed_spinbox.setMaximum(10.000000000000000)
        self.speed_spinbox.setSingleStep(0.250000000000000)
        self.speed_spinbox.setValue(1.000000000000000)

        self.gridLayout.addWidget(self.speed_spinbox, 0, 1, 1, 1)


        self.retranslateUi(playback_settings_dialog)

        QMetaObject.connectSlotsByName(playback_settings_dialog)
    # setupUi

    def retranslateUi(self, playback_settings_dialog):
        playback_settings_dialog.setWindowTitle(QCoreApplication.translate("playback_settings_dialog", u"Dialog", None))
        self.speed_label.setText(QCoreApplication.translate("playback_settings_dialog", u"Playback Speed:", None))
    # retranslateUi

