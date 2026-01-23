from pathlib import Path

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
