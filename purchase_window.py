from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QMessageBox, QScrollArea, QWidget)
from PySide6.QtCore import Qt

class PassengerForm(QWidget):
    def __init__(self, number, parent=None):
        super().__init__(parent)
        self.setup_ui(number)
    
    def setup_ui(self, number):
        layout = QVBoxLayout()
        
        # Заголовок для формы пассажира
        title = QLabel(f"Пассажир {number}")
        title.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("ФИО пассажира")
        layout.addWidget(QLabel("ФИО пассажира:"))
        layout.addWidget(self.name_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Номер телефона")
        layout.addWidget(QLabel("Телефон:"))
        layout.addWidget(self.phone_input)
        
        layout.addSpacing(10)  # Добавляем отступ между формами пассажиров
        self.setLayout(layout)
    
    def get_passenger_info(self):
        return {
            'name': self.name_input.text(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text()
        }

class PurchaseDialog(QDialog):
    def __init__(self, parent=None, flight_data=None):
        super().__init__(parent)
        self.flight_data = flight_data
        self.passenger_forms = []
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Покупка билета")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        
        main_layout = QVBoxLayout()
        
        # Flight info
        if self.flight_data:
            info_text = f"""
            Рейс: {self.flight_data['airline']}
            Откуда: {self.flight_data['origin']}
            Куда: {self.flight_data['destination']}
            Дата: {self.flight_data['date']}
            Время вылета: {self.flight_data['departure']}
            Время прилета: {self.flight_data['arrival']}
            Цена: {self.flight_data['price']} ₽
            Количество пассажиров: {self.flight_data.get('passengers', 1)}
            """
            info_label = QLabel(info_text)
            main_layout.addWidget(info_label)
        
        # Создаем прокручиваемую область для форм пассажиров
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Создаем формы для каждого пассажира
        num_passengers = self.flight_data.get('passengers', 1) if self.flight_data else 1
        for i in range(num_passengers):
            passenger_form = PassengerForm(i + 1)
            self.passenger_forms.append(passenger_form)
            scroll_layout.addWidget(passenger_form)
        
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("Подтвердить")
        self.confirm_button.clicked.connect(self.validate_and_accept)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # Apply styling
        self.setStyleSheet("""
            QDialog {
                background-color: #2b5876;
            }
            QLabel {
                color: white;
                font-size: 14px;
                padding: 5px;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #4e4376;
                border-radius: 4px;
                background-color: white;
                color: black;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4e4376;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5e5386;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #4e4376;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background-color: #5e5386;
                border-radius: 6px;
            }
        """)
    
    def validate_and_accept(self):
        # Проверяем, что все формы заполнены
        for i, form in enumerate(self.passenger_forms):
            info = form.get_passenger_info()
            if not all(info.values()):
                QMessageBox.warning(self, "Ошибка", f"Пожалуйста, заполните все поля для пассажира {i + 1}")
                return
        self.accept()
    
    def get_passenger_info(self):
        return [form.get_passenger_info() for form in self.passenger_forms]
