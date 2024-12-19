import sys
from PySide6.QtWidgets import QApplication
from auth_windows import LoginWindow
from mainwindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Создаем главное окно, но не показываем его
    main_window = MainWindow()
    
    # Показываем окно авторизации
    login_window = LoginWindow(main_window)
    login_window.show()
    
    sys.exit(app.exec())
