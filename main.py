import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
#from PySide6.QtGui import *

from pathlib import Path


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.InitMainWindow()

    def InitMainWindow(self):
        self.setWindowTitle("Popcorn")
        self.resize(500, 300)
        central = QWidget()
        central.setObjectName("central")
        central.setAttribute(Qt.WA_StyledBackground, True)
        self.setCentralWidget(central)

        label = QLabel(central)
        label.setText("popcorn")


def load_qss(filename: str) -> str:
    qss_path = Path(__file__).parent / filename
    return qss_path.read_text(encoding="utf-8")


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(load_qss("style.qss"))
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
