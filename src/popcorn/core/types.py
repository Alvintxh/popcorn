from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LyricsOptions:
    topic: str
    genre: str
    mood: str
    language: str
    length: str  # short|medium|long
    rhyme: bool


@dataclass
class LyricsResult:
    title: str
    lyrics_markdown: str
    model: str
    provider: str
