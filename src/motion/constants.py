"""Motion detection constants."""

from enum import Enum

class MotionDirection(str, Enum):
    """Direction of detected motion."""
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    UNKNOWN = "unknown" 