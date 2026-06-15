"""
Vocabulary Constants & Default Sign Definitions.
"""

from typing import List, Dict, Any

DEFAULT_SIGNS: List[Dict[str, Any]] = [
    # Conversational Words & Signs
    {
        "symbol": "HELLO",
        "label": "Hello / Greeting",
        "category": "word",
        "description": "Flat open hand raised upright facing the camera in a friendly waving salute.",
        "tips": "Extend all 5 fingers upright with thumb spread naturally."
    },
    {
        "symbol": "THANK_YOU",
        "label": "Thank You",
        "category": "word",
        "description": "Flat hand moving forward from chin toward conversational partner.",
        "tips": "Keep fingers together and tilt hand forward toward the screen."
    },
    {
        "symbol": "YES",
        "label": "Yes",
        "category": "word",
        "description": "Closed fist mimicking a nodding head.",
        "tips": "Curl all fingers tightly into a fist with thumb across fingers."
    },
    {
        "symbol": "NO",
        "label": "No",
        "category": "word",
        "description": "Index and middle fingers snapping down to touch thumb tip (like a beak).",
        "tips": "Bring index and middle tips together against thumb tip; curl other fingers."
    },
    {
        "symbol": "I_LOVE_YOU",
        "label": "I Love You",
        "category": "word",
        "description": "ASL ILY sign: thumb, index, and pinky extended simultaneously.",
        "tips": "Keep middle and ring fingers curled down tightly into palm."
    },
    {
        "symbol": "HELP",
        "label": "Help",
        "category": "word",
        "description": "Thumbs-up gesture with thumb pointing straight up.",
        "tips": "Curl four fingers tightly into palm and point thumb straight upward."
    },
    {
        "symbol": "GOOD",
        "label": "Good / OK",
        "category": "word",
        "description": "Index fingertip and thumb tip touching to form a circle with other three fingers upright.",
        "tips": "Form a crisp 'O' with thumb and index; extend middle, ring, and pinky."
    },
    {
        "symbol": "PEACE",
        "label": "Peace / Victory",
        "category": "word",
        "description": "Index and middle fingers extended in a 'V' shape.",
        "tips": "Spread index and middle apart; tuck ring and pinky with thumb."
    },
    {
        "symbol": "STOP",
        "label": "Stop",
        "category": "word",
        "description": "Open hand held forward with fingers held tightly together and thumb tucked.",
        "tips": "Press all fingers side-by-side with palm facing directly forward."
    },
    # Control Actions
    {
        "symbol": "CLEAR",
        "label": "Clear Transcript",
        "category": "control",
        "description": "Horizontal hand wipe gesture to reset and clear the active sentence transcript.",
        "tips": "Tilt hand horizontally sideways across the camera frame."
    },
]
