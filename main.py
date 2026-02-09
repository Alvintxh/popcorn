import sys

from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QSizePolicy
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.windowTitle = "Popcorn Music"
        self.windowWidth = 500
        self.windowHeight = 300
        self.InitMainWindow()

    def InitMainWindow(self):
        self.setWindowTitle(self.windowTitle)
        self.resize(self.windowWidth, self.windowHeight)
        central = QWidget()
        central.setObjectName("central")
        central.setAttribute(Qt.WA_StyledBackground, True)
        self.setCentralWidget(central)

        label = QLabel()
        label.setText("popcorn")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QGridLayout(central)
        layout.addWidget(label)


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
