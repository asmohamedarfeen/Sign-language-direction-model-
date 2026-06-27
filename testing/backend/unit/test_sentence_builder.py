"""
Unit Tests for Sentence Builder & Temporal Debouncer.
"""

from backend.recognition.service.sentence_builder import SentenceBuilder
from backend.recognition.constants import (
    DEBOUNCE_CONSECUTIVE_FRAMES,
    TOKEN_CLEAR,
)


def test_debouncer_accumulation():
    builder = SentenceBuilder()
    session = builder.get_or_create("test_session_1")

    # Send 'HELLO' less than DEBOUNCE_CONSECUTIVE_FRAMES
    for _ in range(DEBOUNCE_CONSECUTIVE_FRAMES - 1):
        committed, text = session.update("HELLO")
        assert not committed
        assert text == ""

    # Reaching threshold commits 'HELLO'
    committed, text = session.update("HELLO")
    assert committed
    assert text.strip() == "Hello"

    # Holding the exact same sign must not spam 'Hello Hello Hello'
    for _ in range(5):
        committed, text = session.update("HELLO")
        assert not committed
        assert text.strip() == "Hello"


def test_word_concatenation():
    builder = SentenceBuilder()
    session = builder.get_or_create("test_session_2")

    # Commit 'HELLO'
    for _ in range(DEBOUNCE_CONSECUTIVE_FRAMES):
        session.update("HELLO")

    # Commit 'THANK_YOU'
    for _ in range(DEBOUNCE_CONSECUTIVE_FRAMES):
        session.update("THANK_YOU")

    assert "Hello" in session.sentence
    assert "Thank you" in session.sentence


def test_clear_action():
    builder = SentenceBuilder()
    session = builder.get_or_create("test_session_3")
    session.sentence = "Hello Thank you"

    for _ in range(DEBOUNCE_CONSECUTIVE_FRAMES):
        session.update(TOKEN_CLEAR)
    assert session.sentence == ""
