from __future__ import annotations

import asyncio
from dataclasses import asdict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QWidget,
)

from ..core.llm_moonshot import MoonshotClient
from ..core.types import LyricsOptions


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Popcorn Music — Lyrics")
        self.resize(980, 720)

        self._client = MoonshotClient()
        self._build_ui()

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("central")
        central.setAttribute(Qt.WA_StyledBackground, True)
        self.setCentralWidget(central)

        layout = QGridLayout(central)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setHorizontalSpacing(16)
        layout.setVerticalSpacing(12)

        header = QLabel("Popcorn Music")
        header.setStyleSheet("font-size: 22px; font-weight: 700;")
        sub = QLabel("Generate song lyrics (title + Verse/Chorus/Bridge) with an LLM.")
        sub.setStyleSheet("color: rgba(255,255,255,0.65);")

        layout.addWidget(header, 0, 0, 1, 2)
        layout.addWidget(sub, 1, 0, 1, 2)

        # Controls
        controls = QGroupBox("Settings")
        c = QGridLayout(controls)
        c.setHorizontalSpacing(10)
        c.setVerticalSpacing(10)

        self.topic = QLineEdit()
        self.topic.setPlaceholderText("e.g., Rainy neon street chase")

        self.genre = QComboBox()
        self.genre.addItems(["Pop", "Rap", "R&B", "Rock", "Folk", "EDM", "Lo-fi", "Ballad"])

        self.mood = QComboBox()
        self.mood.addItems(["Warm", "Sad", "Hopeful", "Energetic", "Dark", "Dreamy", "Funny"])

        self.language = QComboBox()
        self.language.addItems(["Chinese", "English", "Bilingual"])

        self.length = QComboBox()
        self.length.addItems(["short", "medium", "long"])
        self.length.setCurrentText("medium")

        self.rhyme = QCheckBox("Prefer rhymes")
        self.rhyme.setChecked(True)

        self.model = QLineEdit("moonshot-v1-8k")

        self.btn_generate = QPushButton("Generate")
        self.btn_generate.clicked.connect(self.on_generate)  # type: ignore

        self.btn_copy = QPushButton("Copy markdown")
        self.btn_copy.clicked.connect(self.on_copy)  # type: ignore

        row = 0
        c.addWidget(QLabel("Topic"), row, 0)
        c.addWidget(self.topic, row, 1)
        row += 1

        c.addWidget(QLabel("Genre"), row, 0)
        c.addWidget(self.genre, row, 1)
        row += 1

        c.addWidget(QLabel("Mood"), row, 0)
        c.addWidget(self.mood, row, 1)
        row += 1

        c.addWidget(QLabel("Language"), row, 0)
        c.addWidget(self.language, row, 1)
        row += 1

        c.addWidget(QLabel("Length"), row, 0)
        c.addWidget(self.length, row, 1)
        row += 1

        c.addWidget(QLabel("Model"), row, 0)
        c.addWidget(self.model, row, 1)
        row += 1

        c.addWidget(self.rhyme, row, 0, 1, 2)
        row += 1

        btns = QHBoxLayout()
        btns.addWidget(self.btn_generate)
        btns.addWidget(self.btn_copy)
        btns.addStretch(1)
        c.addLayout(btns, row, 0, 1, 2)

        # Output
        self.output = QPlainTextEdit()
        self.output.setPlaceholderText("Generated lyrics will appear here...")

        layout.addWidget(controls, 2, 0)
        layout.addWidget(self.output, 2, 1)
        layout.setColumnStretch(1, 1)

        # Key status
        if not self._client.is_configured():
            warn = QLabel("MOONSHOT_API_KEY not set — Generate will fail until configured.")
            warn.setStyleSheet("color: #ffb020;")
            layout.addWidget(warn, 3, 0, 1, 2)

    def _collect_options(self) -> LyricsOptions:
        return LyricsOptions(
            topic=self.topic.text().strip() or "A song about everyday life",
            genre=self.genre.currentText(),
            mood=self.mood.currentText(),
            language=self.language.currentText(),
            length=self.length.currentText(),
            rhyme=self.rhyme.isChecked(),
        )

    def on_copy(self) -> None:
        text = self.output.toPlainText().strip()
        if not text:
            return
        QApplication.clipboard().setText(text)

    def on_generate(self) -> None:
        opts = self._collect_options()
        model = self.model.text().strip() or "moonshot-v1-8k"

        self.btn_generate.setEnabled(False)
        self.btn_generate.setText("Generating...")

        try:
            # Simple async bridge
            result = asyncio.run(self._client.generate_lyrics(options=opts, model=model))
            self.output.setPlainText(result.lyrics_markdown)
        except Exception as e:
            QMessageBox.critical(self, "Generate failed", str(e))
        finally:
            self.btn_generate.setEnabled(True)
            self.btn_generate.setText("Generate")

        # For future: store history
        _ = asdict(opts)
