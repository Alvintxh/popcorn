import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtWidgets import QLabel
#from PySide6.QtCore import *
#from PySide6.QtGui import *


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.InitMainWindow()

    def InitMainWindow(self):
        self.setWindowTitle("Popcorn")
        self.resize(500, 300)
        central = QWidget()
        self.setCentralWidget(central)

        label = QLabel(central)
        label.setText("popcorn")


def main():
    app = QApplication()
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
