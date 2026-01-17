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

