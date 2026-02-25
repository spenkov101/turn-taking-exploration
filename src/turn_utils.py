import re
from typing import List, Optional
from collections import Counter, defaultdict
TOKEN_RE = re.compile(r"\w+|[^\w\s]")

def last_token(text: str) -> str:
    """
    Return the last token (word or punctuation) of a given utterance.

    Helpful for early turn-taking feature analysis.
    """
    if not text:
        return ""
    tokens = TOKEN_RE.findall(text.strip())
    return tokens[-1].lower() if tokens else ""

def turn_last_tokens(dialogue: List[str], n: Optional[int] = None) -> List[str]:
    """
    Given a list of utterances (dialogue), return last tokens for each turn.
    If n is provided, limit to first n turns.
    """
    selected = dialogue if n is None else dialogue[:n]
    return [last_token(utt) for utt in selected]



def last_token_frequency(dialogues):
    """
    Compute frequency of last tokens across all turns
    in a list of dialogue dicts.
    """
    freq = Counter()

    for d in dialogues:
        for turn in d["turns"]:
            token = last_token(turn["text"])
            if token:
                freq[token] += 1

    return freq

def question_ratio(dialogues):
    """
    Compute how many turns end with a question mark.
    Returns (num_questions, total_turns, ratio).
    """
    total = 0
    questions = 0

    for d in dialogues:
        for turn in d["turns"]:
            total += 1
            if turn["text"].strip().endswith("?"):
                questions += 1

    ratio = questions / total if total > 0 else 0.0
    return questions, total, ratio
def avg_turn_length_by_type(dialogues):
    """
    Compute average turn length (in tokens) for
    question-ending vs non-question turns.
    """
    q_len = 0
    q_count = 0
    s_len = 0
    s_count = 0

    for d in dialogues:
        for turn in d["turns"]:
            tokens = turn["text"].split()
            if not tokens:
                continue

            if turn["text"].strip().endswith("?"):
                q_len += len(tokens)
                q_count += 1
            else:
                s_len += len(tokens)
                s_count += 1

    avg_q = q_len / q_count if q_count else 0.0
    avg_s = s_len / s_count if s_count else 0.0

    return avg_q, avg_s

def speaker_alternation_rate(dialogues):
    """
    Compute how often consecutive turns switch speakers.
    Returns (num_switches, total_transitions, rate).
    """
    switches = 0
    transitions = 0

    for d in dialogues:
        turns = d["turns"]
        for i in range(1, len(turns)):
            transitions += 1
            if turns[i]["speaker"] != turns[i - 1]["speaker"]:
                switches += 1

    rate = switches / transitions if transitions > 0 else 0.0
    return switches, transitions, rate


def avg_turn_length_per_speaker(dialogues):
    """
    Compute average turn length (in tokens) per speaker.
    Returns dict: {speaker: avg_length}
    """
    totals = defaultdict(int)
    counts = defaultdict(int)

    for d in dialogues:
        for turn in d["turns"]:
            tokens = turn["text"].split()
            if not tokens:
                continue
            spk = turn["speaker"]
            totals[spk] += len(tokens)
            counts[spk] += 1

    return {spk: totals[spk] / counts[spk] for spk in counts}



def turn_final_punctuation(dialogues):
    """
    Count how often turns end with '.', '?', '!', or other.
    Returns a Counter.
    """
    counts = Counter()

    for d in dialogues:
        for turn in d["turns"]:
            text = turn["text"].strip()
            if not text:
                continue

            last_char = text[-1]
            if last_char in {".", "?", "!"}:
                counts[last_char] += 1
            else:
                counts["other"] += 1

    return counts

def ending_vs_speaker_switch(dialogues):
    """
    Analyze whether certain turn endings correlate with speaker switches.

    Returns:
        dict: {
            ending_type: {
                "switches": int,
                "total": int,
                "switch_rate": float
            }
        }
    """
    stats = defaultdict(lambda: {"switches": 0, "total": 0})

    for d in dialogues:
        turns = d["turns"]

        for i in range(len(turns) - 1):
            current = turns[i]
            nxt = turns[i + 1]

            text = current["text"].strip()
            if not text:
                continue

            last_char = text[-1]
            if last_char not in {".", "?", "!"}:
                last_char = "other"

            stats[last_char]["total"] += 1
            if current["speaker"] != nxt["speaker"]:
                stats[last_char]["switches"] += 1

    # compute rates
    for ending in stats:
        total = stats[ending]["total"]
        switches = stats[ending]["switches"]
        stats[ending]["switch_rate"] = switches / total if total else 0.0

    return dict(stats)

def turn_length_list(dialogues):
    """
    Return a list of turn lengths (in tokens) across all dialogues.
    Useful for later distribution analysis.
    """
    lengths = []

    for d in dialogues:
        for turn in d["turns"]:
            tokens = turn["text"].split()
            if tokens:
                lengths.append(len(tokens))

    return lengths

FILLERS = {"uh", "um", "erm", "hmm"}

def filler_before_switch(dialogues):
    """
    Check how often turns ending with a filler are followed by a speaker switch.

    Returns:
        {
            "filler_turns": int,
            "switch_after_filler": int,
            "switch_rate": float
        }
    """
    filler_turns = 0
    switch_after_filler = 0

    for d in dialogues:
        turns = d["turns"]

        for i in range(len(turns) - 1):
            current = turns[i]["text"].strip().lower()
            next_speaker = turns[i + 1]["speaker"]
            curr_speaker = turns[i]["speaker"]

            tokens = current.split()
            if not tokens:
                continue

            if tokens[-1].strip(".,!?") in FILLERS:
                filler_turns += 1
                if curr_speaker != next_speaker:
                    switch_after_filler += 1

    rate = switch_after_filler / filler_turns if filler_turns else 0.0

    return {
        "filler_turns": filler_turns,
        "switch_after_filler": switch_after_filler,
        "switch_rate": rate
    }
def count_fillers(dialogues):
    """
    Count occurrences of filler words within turns.
    Returns total filler count and per-speaker counts.
    """
    FILLERS = {"uh", "um", "erm", "hmm"}
    total = 0
    per_speaker = {}

    for d in dialogues:
        for turn in d["turns"]:
            spk = turn["speaker"]
            text = turn["text"].lower()

            tokens = [t.strip(".,!?") for t in text.split()]
            count = sum(1 for t in tokens if t in FILLERS)

            if count > 0:
                total += count
                per_speaker[spk] = per_speaker.get(spk, 0) + count
def response_length_ratio(dialogues):
    """
    Compute distribution of response length ratios.

    Ratio = len(next_turn) / len(current_turn)

    Returns:
        {
            "avg_ratio": float,
            "ratios": list[float]
        }
    """
    ratios = []

    for d in dialogues:
        turns = d["turns"]

        for i in range(len(turns) - 1):
            curr_tokens = turns[i]["text"].split()
            next_tokens = turns[i + 1]["text"].split()

            if not curr_tokens or not next_tokens:
                continue

            ratio = len(next_tokens) / len(curr_tokens)
            ratios.append(ratio)

    avg_ratio = sum(ratios) / len(ratios) if ratios else 0.0

    return {
        "avg_ratio": avg_ratio,
        "ratios": ratios
    }
    return {
        "total_fillers": total,
        "per_speaker": per_speaker
    }
