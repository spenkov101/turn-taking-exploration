import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def load_local_dialogues(filename: str = "sample_dialogues.json"):
    """
    Load local dialogue data for turn-taking exploration.
    """
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
