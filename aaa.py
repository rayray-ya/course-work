from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QHBoxLayout,
                               QLabel, QLineEdit, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 400)
        MainWindow.setMinimumSize(QSize(500, 400))
        MainWindow.setMaximumSize(QSize(1920, 1080))
        icon = QIcon("pineapple.ico")
        MainWindow.setWindowIcon(icon)
        MainWindow.setMouseTracking(True)
        MainWindow.setStyleSheet(
            u"background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 50, 150, 255), stop:0.5 rgba(0, 100, 200, 255), stop:1 rgba(100, 150, 255, 255));\n"
            "")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        # Create main vertical layout for centralwidget
        self.main_vertical_layout = QVBoxLayout(self.centralwidget)
        self.main_vertical_layout.setAlignment(Qt.AlignCenter)
        
        # Add title label
        self.title_label = QLabel("AnAvia")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                background: transparent;
            }
        """)
        self.main_vertical_layout.addWidget(self.title_label)
        
        # Create container widget for all content
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 20px;")
        self.content_layout = QVBoxLayout(self.content_widget)
        
        # Move existing widgets to the new layout
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.lineEdit_2 = QLineEdit(self.widget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_2.addWidget(self.lineEdit_2)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.dateEdit = QDateEdit(self.widget)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setMinimumSize(QSize(120, 30))
        self.dateEdit.setStyleSheet("QDateEdit { background-color: rgba(255, 255, 255, 0.2); padding: 5px; border-radius: 5px; }")
        self.dateEdit.setCalendarPopup(True)

        self.horizontalLayout_4.addWidget(self.dateEdit)

        self.dateEdit_2 = QDateEdit(self.widget)
        self.dateEdit_2.setObjectName(u"dateEdit_2")
        self.dateEdit_2.setMinimumSize(QSize(120, 30))
        self.dateEdit_2.setStyleSheet("QDateEdit { background-color: rgba(255, 255, 255, 0.2); padding: 5px; border-radius: 5px; }")
        self.dateEdit_2.setCalendarPopup(True)

        self.horizontalLayout_4.addWidget(self.dateEdit_2)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.comboBox = QComboBox(self.widget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(120, 30))
        self.comboBox.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 0.2);
                padding: 5px;
                border-radius: 5px;
            }
            QComboBox:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: rgb(40, 80, 150);
                selection-background-color: rgb(60, 100, 170);
                color: white;
                border: none;
                outline: none;
            }
        """)

        self.verticalLayout_3.addWidget(self.comboBox)

        self.comboBox_2 = QComboBox(self.widget)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setMinimumSize(QSize(120, 30))
        self.comboBox_2.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 0.2);
                padding: 5px;
                border-radius: 5px;
            }
            QComboBox:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: rgb(40, 80, 150);
                selection-background-color: rgb(60, 100, 170);
                color: white;
                border: none;
                outline: none;
            }
        """)

        self.verticalLayout_3.addWidget(self.comboBox_2)

        self.horizontalLayout_5.addLayout(self.verticalLayout_3)

        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        
        # Add widget to content layout
        self.content_layout.addWidget(self.widget)
        
        # Add pushButton to content layout
        self.pushButton = QPushButton(self.content_widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(200, 40))
        font = QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(0, 122, 204);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: rgb(0, 136, 228);
            }
            QPushButton:pressed {
                background-color: rgb(0, 108, 180);
            }
        """)
        self.content_layout.addWidget(self.pushButton)
        
        # Add content widget to main layout
        self.main_vertical_layout.addWidget(self.content_widget)
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"AnAvia", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow",
                                                           u"\u041d\u0430\u0439\u0442\u0438 \u0431\u0438\u043b\u0435\u0442\u044b",
                                                           None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0443\u0434\u0430", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0443\u0434\u0430", None))
        self.lineEdit_2.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u0433\u0434\u0430", None))
        self.label_5.setText(
            QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u0442\u043d\u043e", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow",
                                                                u"1 \u043f\u0430\u0441\u0441\u0430\u0436\u0438\u0440",
                                                                None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow",
                                                                u"2 \u043f\u0430\u0441\u0441\u0430\u0436\u0438\u0440\u0430",
                                                                None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow",
                                                                u"3 \u043f\u0430\u0441\u0441\u0430\u0436\u0438\u0440\u0430",
                                                                None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow",
                                                                u"4 \u043f\u0430\u0441\u0441\u0430\u0436\u0438\u0440\u0430",
                                                                None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow",
                                                                u"5 \u043f\u0430\u0441\u0441\u0430\u0436\u0438\u0440\u043e\u0432",
                                                                None))

        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"\u042d\u043a\u043e\u043d\u043e\u043c",
                                                                  None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow",
                                                                  u"\u041a\u043e\u043c\u0444\u043e\u0440\u0442", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("MainWindow", u"\u0411\u0438\u0437\u043d\u0435\u0441",
                                                                  None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("MainWindow",
                                                                  u"\u041f\u0435\u0440\u0432\u044b\u0439 \u043a\u043b\u0430\u0441\u0441",
                                                                  None))
