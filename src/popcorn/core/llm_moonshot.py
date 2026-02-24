from __future__ import annotations

import os

import httpx

from .types import LyricsOptions, LyricsResult


class MoonshotClient:
    def __init__(self, api_key: str | None = None, base_url: str = "https://api.moonshot.cn/v1"):
        self.api_key = api_key or os.getenv("MOONSHOT_API_KEY")
        self.base_url = base_url.rstrip("/")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def generate_lyrics(self, *, options: LyricsOptions, model: str = "moonshot-v1-8k") -> LyricsResult:
        if not self.api_key:
            raise RuntimeError("MOONSHOT_API_KEY is not set. Please set it in your environment.")

        system = (
            "You are a songwriting assistant. Produce a complete song lyric in markdown. "
            "Return ONLY markdown. Use headings for sections."
        )

        rhyme = "with consistent end rhymes" if options.rhyme else "no strict rhyme required"
        prompt = (
            f"Write a {options.length} song lyric in {options.language}.\n"
            f"Topic: {options.topic}\nGenre: {options.genre}\nMood: {options.mood}\n"
            f"Constraints: {rhyme}.\n\n"
            "Structure:\n"
            "# <Title>\n"
            "## Verse 1\n...\n"
            "## Chorus\n...\n"
            "## Verse 2\n...\n"
            "## Chorus\n...\n"
            "## Bridge\n...\n"
            "## Final Chorus\n...\n"
        )

        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.9,
                },
            )
            if r.status_code >= 400:
                raise RuntimeError(f"Moonshot API error {r.status_code}: {r.text[:500]}")

            data = r.json()
            content = data["choices"][0]["message"]["content"]

        # crude title extraction
        title = "Untitled"
        for line in content.splitlines():
            if line.strip().startswith("# "):
                title = line.strip()[2:].strip() or title
                break

        return LyricsResult(title=title, lyrics_markdown=content.strip(), model=model, provider="moonshot")
