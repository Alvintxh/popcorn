import sys
from PySide6.QtWidgets import QApplication, QMainWindow
#from PySide6.QtCore import *
#from PySide6.QtGui import *


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()


if __name__ == "__main__":
    app = QApplication()
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
