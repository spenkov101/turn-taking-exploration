from datasets import load_dataset

def load_multiwoz(split: str = "train"):
    """
    Load the MultiWOZ 2.2 dialogue dataset.

    Script-free, stable, and suitable for turn-taking exploration.
    """
    return load_dataset("multi_woz_v22", split=split)
