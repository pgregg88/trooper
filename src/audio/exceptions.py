"""Custom exceptions for audio processing."""

class AudioError(Exception):
    """Base exception for audio processing errors."""

class AudioPlaybackError(AudioError):
    """Exception raised when audio playback fails."""

class AudioProcessingError(AudioError):
    """Exception raised when audio processing fails."""

class AudioFileError(AudioError):
    """Exception raised when there are issues with audio files.""" 