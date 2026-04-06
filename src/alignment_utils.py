from pathlib import Path

from src.audio_utils import get_wav_duration


def align_turns_with_audio(turns, audio_dir: str | Path):
    """
    Align dialogue turns with WAV audio files by sorted order.

    Assumes:
    - each WAV file corresponds to one turn
    - files are named in turn order
    - number of audio files matches number of turns, or alignment
      is performed up to the shortest length

    Args:
        turns (list of dict):
            [
                {"speaker": "A", "text": "Hi"},
                {"speaker": "B", "text": "Hello"},
            ]
        audio_dir (str | Path):
            Directory containing turn-level WAV files.

    Returns:
        list of dict:
            [
                {
                    "speaker": "A",
                    "text": "Hi",
                    "audio_file": "turn_001.wav",
                    "duration": 0.82,
                },
                ...
            ]
    """
    audio_dir = Path(audio_dir)

    audio_files = sorted(
        file for file in audio_dir.iterdir()
        if file.suffix.lower() == ".wav"
    ) if audio_dir.exists() else []

    aligned = []

    for turn, audio_file in zip(turns, audio_files):
        aligned.append({
            "speaker": turn["speaker"],
            "text": turn["text"],
            "audio_file": audio_file.name,
            "duration": get_wav_duration(audio_file),
        })

    return aligned