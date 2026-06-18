"""
Sentence Builder & Temporal Debouncer.

Maintains session state, stabilizes predictions over consecutive frames,
and constructs coherent English sentences from continuous sign gestures.
"""

from typing import Dict, Optional, Tuple
from backend.recognition.constants import (
    DEBOUNCE_CONSECUTIVE_FRAMES,
    TOKEN_CLEAR,
    WHOLE_WORD_SIGNS,
)


class SessionState:
    """State tracked for an active translation session."""

    def __init__(self, session_id: str):
        self.session_id: str = session_id
        self.sentence: str = ""
        self.last_candidate: Optional[str] = None
        self.candidate_streak: int = 0
        self.last_committed_sign: Optional[str] = None

    def reset(self) -> None:
        """Clears the current accumulated sentence."""
        self.sentence = ""
        self.last_candidate = None
        self.candidate_streak = 0
        self.last_committed_sign = None

    def update(self, sign: str) -> Tuple[bool, str]:
        """
        Updates the temporal window with a new frame's predicted sign.
        Returns (is_new_commitment, updated_sentence).
        """
        if sign == self.last_candidate:
            self.candidate_streak += 1
        else:
            self.last_candidate = sign
            self.candidate_streak = 1

        # Check if gesture reached required stability threshold
        if self.candidate_streak >= DEBOUNCE_CONSECUTIVE_FRAMES:
            # Avoid repeating the exact same sign without releasing / shifting
            if self.last_committed_sign != sign:
                self.commit_sign(sign)
                self.last_committed_sign = sign
                return True, self.sentence

        # If user switches away from the committed sign, reset commitment lock
        if sign != self.last_committed_sign:
            self.last_committed_sign = None

        return False, self.sentence

    def commit_sign(self, sign: str) -> None:
        """Applies sign action to the sentence string."""
        if sign == TOKEN_CLEAR:
            self.sentence = ""
        elif sign in WHOLE_WORD_SIGNS:
            word = WHOLE_WORD_SIGNS[sign]
            if self.sentence and not self.sentence.endswith(" "):
                self.sentence += f" {word} "
            else:
                self.sentence += f"{word} "
        else:
            word = sign.replace("_", " ").title()
            if self.sentence and not self.sentence.endswith(" "):
                self.sentence += f" {word} "
            else:
                self.sentence += f"{word} "


class SentenceBuilder:
    """Session-aware registry of sentence states."""

    def __init__(self):
        self._sessions: Dict[str, SessionState] = {}

    def get_or_create(self, session_id: Optional[str] = None) -> SessionState:
        sid = session_id or "default_session"
        if sid not in self._sessions:
            self._sessions[sid] = SessionState(sid)
        return self._sessions[sid]

    def reset_session(self, session_id: Optional[str] = None) -> str:
        state = self.get_or_create(session_id)
        state.reset()
        return state.sentence
