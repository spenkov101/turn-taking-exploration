from pathlib import Path
import wave
def list_audio_files(audio_dir):
    """
    List audio files in a directory.

    This is a placeholder utility to support future
    turn-taking experiments with audio.
    """
    audio_dir = Path(audio_dir)
    if not audio_dir.exists():
        return []

    return sorted(
        p for p in audio_dir.iterdir()
        if p.suffix.lower() in {".wav", ".mp3", ".flac"}
    )


def get_wav_duration(filepath):
    """
    Get duration (in seconds) of a WAV audio file.

    Returns None if file cannot be read.
    """
    filepath = Path(filepath)

    if filepath.suffix.lower() != ".wav":
        return None

    try:
        with wave.open(str(filepath), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate)
    except Exception:
        return None
