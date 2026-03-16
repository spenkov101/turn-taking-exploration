from pathlib import Path
import wave


def list_audio_files(audio_dir: str | Path):
    """
    List audio files in a directory.

    This is a placeholder utility to support future
    turn-taking experiments with audio.
    """
    audio_dir = Path(audio_dir)

    if not audio_dir.exists():
        return []

    return sorted(
        file for file in audio_dir.iterdir()
        if file.suffix.lower() in {".wav", ".mp3", ".flac"}
    )


def get_wav_duration(filepath: str | Path) -> float | None:
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


def get_turn_durations(audio_dir):
    """
    Compute durations for all WAV audio files in a directory.

    Assumes each file corresponds to a single dialogue turn.

    Returns:
        list of dicts:
        [
            {"file": "turn_001.wav", "duration": 1.24},
            {"file": "turn_002.wav", "duration": 0.87},
        ]
    """
    audio_files = list_audio_files(audio_dir)

    results = []

    for file in audio_files:
        duration = get_wav_duration(file)

        if duration is not None:
            results.append({
                "file": file.name,
                "duration": duration
            })

    return results

def compute_total_speech_time(turns):
    """
    Compute total speech time across all turns.

    Args:
        turns (list of dict):
            [
                {"speaker": "A", "duration": 1.2},
                {"speaker": "B", "duration": 0.8},
                {"speaker": "A", "duration": 2.1},
            ]

    Returns:
        float:
            total speech time in seconds
    """
    total_time = 0.0

    for turn in turns:
        duration = turn.get("duration", 0)
        total_time += duration

    return total_time


def compute_speaker_dominance(turns):
    """
    Compute speaker dominance based on turn durations.

    Args:
        turns (list of dict):
            [
                {"speaker": "A", "duration": 1.2},
                {"speaker": "B", "duration": 0.8},
                {"speaker": "A", "duration": 2.1},
            ]

    Returns:
        dict:
        {
            "A": 0.65,
            "B": 0.35
        }
        Values represent proportion of total speaking time.
    """
    speaker_times = {}
    total_time = 0.0

    for turn in turns:
        speaker = turn["speaker"]
        duration = turn["duration"]

        speaker_times.setdefault(speaker, 0)
        speaker_times[speaker] += duration
        total_time += duration

    if total_time == 0:
        return {}

    return {
        speaker: time / total_time
        for speaker, time in speaker_times.items()
    }

def compute_turn_statistics(turns):
    """
    Compute basic statistics about turn durations.

    Args:
        turns (list of dict):
            [
                {"speaker": "A", "duration": 1.2},
                {"speaker": "B", "duration": 0.8},
            ]

    Returns:
        dict:
        {
            "turn_count": int,
            "avg_turn_length": float,
            "median_turn_length": float,
            "max_turn_length": float
        }
    """
    durations = [turn.get("duration", 0) for turn in turns if turn.get("duration") is not None]

    if not durations:
        return {
            "turn_count": 0,
            "avg_turn_length": 0,
            "median_turn_length": 0,
            "max_turn_length": 0
        }

    durations_sorted = sorted(durations)
    count = len(durations)

    avg = sum(durations) / count
    max_len = max(durations)

    mid = count // 2
    if count % 2 == 0:
        median = (durations_sorted[mid - 1] + durations_sorted[mid]) / 2
    else:
        median = durations_sorted[mid]

    return {
        "turn_count": count,
        "avg_turn_length": avg,
        "median_turn_length": median,
        "max_turn_length": max_len
    }