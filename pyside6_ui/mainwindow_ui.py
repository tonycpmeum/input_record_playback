# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QLabel, QLayout, QMainWindow,
    QMenu, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSpinBox, QStatusBar, QVBoxLayout,
    QWidget)

from modules.model_view import CustomListView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(378, 387)
        MainWindow.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        self.playbackconfig_QAction = QAction(MainWindow)
        self.playbackconfig_QAction.setObjectName(u"playbackconfig_QAction")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setAcceptDrops(False)
        self.gridLayoutWidget_2 = QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(190, 10, 181, 80))
        self.repeat_grid = QGridLayout(self.gridLayoutWidget_2)
        self.repeat_grid.setObjectName(u"repeat_grid")
        self.repeat_grid.setHorizontalSpacing(6)
        self.repeat_grid.setVerticalSpacing(0)
        self.repeat_grid.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.repeat_grid.addWidget(self.label_3, 1, 2, 1, 1)

        self.repeat_label = QLabel(self.gridLayoutWidget_2)
        self.repeat_label.setObjectName(u"repeat_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.repeat_label.sizePolicy().hasHeightForWidth())
        self.repeat_label.setSizePolicy(sizePolicy)

        self.repeat_grid.addWidget(self.repeat_label, 0, 0, 1, 3)

        self.repeat_times_input = QSpinBox(self.gridLayoutWidget_2)
        self.repeat_times_input.setObjectName(u"repeat_times_input")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.repeat_times_input.sizePolicy().hasHeightForWidth())
        self.repeat_times_input.setSizePolicy(sizePolicy1)
        self.repeat_times_input.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.repeat_times_input.setAutoFillBackground(False)
        self.repeat_times_input.setFrame(True)
        self.repeat_times_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.repeat_times_input.setAccelerated(False)
        self.repeat_times_input.setMinimum(1)
        self.repeat_times_input.setMaximum(10000)
        self.repeat_times_input.setValue(1)

        self.repeat_grid.addWidget(self.repeat_times_input, 1, 1, 1, 1)

        self.repeat_stop_radio = QRadioButton(self.gridLayoutWidget_2)
        self.repeat_stop_radio.setObjectName(u"repeat_stop_radio")
        self.repeat_stop_radio.setChecked(True)

        self.repeat_grid.addWidget(self.repeat_stop_radio, 2, 0, 1, 3)

        self.repeat_times_radio = QRadioButton(self.gridLayoutWidget_2)
        self.repeat_times_radio.setObjectName(u"repeat_times_radio")

        self.repeat_grid.addWidget(self.repeat_times_radio, 1, 0, 1, 1)

        self.start_btn = QPushButton(self.centralwidget)
        self.start_btn.setObjectName(u"start_btn")
        self.start_btn.setGeometry(QRect(200, 230, 151, 51))
        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(230, 10, 111, 31))
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(20, 10, 151, 331))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.enable_script_checkbox = QCheckBox(self.verticalLayoutWidget_2)
        self.enable_script_checkbox.setObjectName(u"enable_script_checkbox")
        self.enable_script_checkbox.setAutoRepeat(False)
        self.enable_script_checkbox.setTristate(False)

        self.verticalLayout.addWidget(self.enable_script_checkbox)

        self.script_container = QWidget(self.verticalLayoutWidget_2)
        self.script_container.setObjectName(u"script_container")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.script_container.sizePolicy().hasHeightForWidth())
        self.script_container.setSizePolicy(sizePolicy2)
        self.script_container.setMaximumSize(QSize(16777215, 16777215))
        self.layoutWidget = QWidget(self.script_container)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 149, 281))
        self.script_func_group = QVBoxLayout(self.layoutWidget)
        self.script_func_group.setSpacing(7)
        self.script_func_group.setObjectName(u"script_func_group")
        self.script_func_group.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.script_func_group.setContentsMargins(0, 0, 0, 0)
        self.listView = CustomListView(self.layoutWidget)
        self.listView.setObjectName(u"listView")
        self.listView.setEnabled(True)

        self.script_func_group.addWidget(self.listView)

        self.record_btn = QPushButton(self.layoutWidget)
        self.record_btn.setObjectName(u"record_btn")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.record_btn.sizePolicy().hasHeightForWidth())
        self.record_btn.setSizePolicy(sizePolicy3)
        self.record_btn.setAutoFillBackground(False)
        self.record_btn.setCheckable(False)
        self.record_btn.setChecked(False)
        self.record_btn.setAutoDefault(False)
        self.record_btn.setFlat(False)

        self.script_func_group.addWidget(self.record_btn)

        self.delete_btn = QPushButton(self.layoutWidget)
        self.delete_btn.setObjectName(u"delete_btn")

        self.script_func_group.addWidget(self.delete_btn)


        self.verticalLayout.addWidget(self.script_container)

        self.click_container = QWidget(self.centralwidget)
        self.click_container.setObjectName(u"click_container")
        self.click_container.setGeometry(QRect(180, 90, 191, 111))
        self.line = QFrame(self.click_container)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(80, 0, 81, 41))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.gridLayoutWidget = QWidget(self.click_container)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 162, 96))
        self.click_grid = QGridLayout(self.gridLayoutWidget)
        self.click_grid.setObjectName(u"click_grid")
        self.click_grid.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.click_grid.setHorizontalSpacing(9)
        self.click_grid.setVerticalSpacing(5)
        self.click_grid.setContentsMargins(0, 0, 0, 0)
        self.interval_label = QLabel(self.gridLayoutWidget)
        self.interval_label.setObjectName(u"interval_label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.interval_label.sizePolicy().hasHeightForWidth())
        self.interval_label.setSizePolicy(sizePolicy4)
        self.interval_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.click_grid.addWidget(self.interval_label, 1, 0, 1, 1)

        self.click_label = QLabel(self.gridLayoutWidget)
        self.click_label.setObjectName(u"click_label")
        self.click_label.setEnabled(True)
        self.click_label.setFrameShape(QFrame.Shape.NoFrame)
        self.click_label.setScaledContents(False)
        self.click_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.click_grid.addWidget(self.click_label, 0, 0, 1, 2)

        self.button_label = QLabel(self.gridLayoutWidget)
        self.button_label.setObjectName(u"button_label")
        sizePolicy4.setHeightForWidth(self.button_label.sizePolicy().hasHeightForWidth())
        self.button_label.setSizePolicy(sizePolicy4)
        self.button_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.click_grid.addWidget(self.button_label, 2, 0, 1, 1)

        self.button_combobox = QComboBox(self.gridLayoutWidget)
        self.button_combobox.addItem("")
        self.button_combobox.addItem("")
        self.button_combobox.addItem("")
        self.button_combobox.setObjectName(u"button_combobox")

        self.click_grid.addWidget(self.button_combobox, 2, 1, 1, 1)

        self.click_interval_input = QSpinBox(self.gridLayoutWidget)
        self.click_interval_input.setObjectName(u"click_interval_input")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.click_interval_input.sizePolicy().hasHeightForWidth())
        self.click_interval_input.setSizePolicy(sizePolicy5)
        self.click_interval_input.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.click_interval_input.setAutoFillBackground(False)
        self.click_interval_input.setFrame(True)
        self.click_interval_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.click_interval_input.setAccelerated(False)
        self.click_interval_input.setMinimum(1)
        self.click_interval_input.setMaximum(9999999)
        self.click_interval_input.setValue(100)

        self.click_grid.addWidget(self.click_interval_input, 1, 1, 1, 1)

        self.clicktype_combobox = QComboBox(self.gridLayoutWidget)
        self.clicktype_combobox.addItem("")
        self.clicktype_combobox.addItem("")
        self.clicktype_combobox.setObjectName(u"clicktype_combobox")

        self.click_grid.addWidget(self.clicktype_combobox, 3, 1, 1, 1)

        self.clicktype_label = QLabel(self.gridLayoutWidget)
        self.clicktype_label.setObjectName(u"clicktype_label")
        sizePolicy4.setHeightForWidth(self.clicktype_label.sizePolicy().hasHeightForWidth())
        self.clicktype_label.setSizePolicy(sizePolicy4)
        self.clicktype_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.click_grid.addWidget(self.clicktype_label, 3, 0, 1, 1)

        self.stop_btn = QPushButton(self.centralwidget)
        self.stop_btn.setObjectName(u"stop_btn")
        self.stop_btn.setGeometry(QRect(200, 290, 151, 31))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 378, 22))
        self.menusettings = QMenu(self.menubar)
        self.menusettings.setObjectName(u"menusettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menusettings.menuAction())
        self.menusettings.addAction(self.playbackconfig_QAction)

        self.retranslateUi(MainWindow)

        self.start_btn.setDefault(False)
        self.record_btn.setDefault(False)
        self.stop_btn.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.playbackconfig_QAction.setText(QCoreApplication.translate("MainWindow", u"Pl&ayback config", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"times", None))
        self.repeat_label.setText(QCoreApplication.translate("MainWindow", u"Repeat", None))
        self.repeat_stop_radio.setText(QCoreApplication.translate("MainWindow", u"Repeat until stopped", None))
        self.repeat_times_radio.setText(QCoreApplication.translate("MainWindow", u"Repeat", None))
        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.enable_script_checkbox.setText(QCoreApplication.translate("MainWindow", u"&Enable Script Playback", None))
        self.record_btn.setText(QCoreApplication.translate("MainWindow", u"Record", None))
        self.delete_btn.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.interval_label.setText(QCoreApplication.translate("MainWindow", u"Interval (ms)", None))
        self.click_label.setText(QCoreApplication.translate("MainWindow", u"Click options", None))
        self.button_label.setText(QCoreApplication.translate("MainWindow", u"Mouse button", None))
        self.button_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"Left", None))
        self.button_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"Right", None))
        self.button_combobox.setItemText(2, QCoreApplication.translate("MainWindow", u"Middle", None))

        self.clicktype_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"Single", None))
        self.clicktype_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"Double", None))

        self.clicktype_label.setText(QCoreApplication.translate("MainWindow", u"Click type", None))
        self.stop_btn.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.menusettings.setTitle(QCoreApplication.translate("MainWindow", u"&Settings", None))
    # retranslateUi

