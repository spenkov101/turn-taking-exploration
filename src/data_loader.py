from datasets import load_dataset

def load_dailydialog(split: str = "train"):
    """
    Load the DailyDialog dataset.

    Explicitly allow legacy dataset scripts.
    """
    return load_dataset(
        "daily_dialog",
        split=split,
        trust_remote_code=True
    )
