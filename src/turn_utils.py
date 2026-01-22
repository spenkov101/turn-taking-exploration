import re
from typing import List, Optional
from collections import Counter
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
