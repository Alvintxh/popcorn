# Popcorn Music

A desktop GUI for generating song lyrics with an LLM.

## Run (dev)

```bash
cd projects/popcorn
python -m venv .venv
source .venv/bin/activate
pip install -e .

# set your key (recommended)
export MOONSHOT_API_KEY=... 

popcorn
```

## Notes

- V0 focuses on lyrics generation (title + Verse/Chorus/Bridge) and export.
- Melody/audio generation is out of scope for now.
