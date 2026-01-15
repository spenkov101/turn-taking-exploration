from datasets import load_dataset

def load_dailydialog(split: str = "train"):
    """
    Load the DailyDialog dataset (explicit config).
    """
    return load_dataset(
        "daily_dialog",
        name="dialog",
        split=split,
        trust_remote_code=True
    )
