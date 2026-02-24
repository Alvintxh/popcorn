import sys

from PySide6.QtWidgets import QApplication

from .ui.main_window import MainWindow
from .util.qss import load_qss


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(load_qss("style.qss"))
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())
