from datasets import load_dataset

def load_dailydialog(split: str = "train"):
    """
    Load the DailyDialog dataset.

    Returns a HuggingFace Dataset object.
    Each item contains:
      - dialog: list[str]
      - act: list[int]
      - emotion: list[int]
    """
    return load_dataset("daily_dialog", split=split)
