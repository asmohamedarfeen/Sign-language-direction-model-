"""
Recognition Module Constants.
"""

# Default inference thresholds
DEFAULT_CONFIDENCE_THRESHOLD: float = 0.65
DEBOUNCE_CONSECUTIVE_FRAMES: int = 5
MAX_HISTORY_BUFFER_FRAMES: int = 30

# Special control tokens
TOKEN_CLEAR: str = "CLEAR"
TOKEN_NOTHING: str = "NOTHING"

WHOLE_WORD_SIGNS = {
    "HELLO": "Hello",
    "THANK_YOU": "Thank you",
    "YES": "Yes",
    "NO": "No",
    "I_LOVE_YOU": "I love you",
    "HELP": "Help",
    "GOOD": "Good",
    "PEACE": "Peace",
    "STOP": "Stop",
}
