import re
from typing import List, Optional

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

