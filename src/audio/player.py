"""Audio playback functionality."""

import os
from pathlib import Path
from typing import Optional
import sounddevice as sd
import soundfile as sf
from loguru import logger

class AudioPlayer:
    """Audio playback handler."""
    
    def __init__(self):
        """Initialize the audio player."""
        self.current_file = None
        logger.info("Initialized audio player")
    
    def play_file(self, file_path: str) -> bool:
        """Play an audio file.
        
        Args:
            file_path: Path to the audio file to play
            
        Returns:
            True if playback successful, False otherwise
        """
        try:
            # Load the audio file
            data, samplerate = sf.read(file_path)
            
            # Play the audio
            sd.play(data, samplerate)
            sd.wait()  # Wait until file is done playing
            
            self.current_file = file_path
            logger.info(f"Played audio file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to play audio: {str(e)}")
            return False
    
    def stop(self):
        """Stop current playback."""
        try:
            sd.stop()
            logger.info("Stopped audio playback")
        except Exception as e:
            logger.error(f"Failed to stop playback: {str(e)}")
    
    @property
    def is_playing(self) -> bool:
        """Check if audio is currently playing."""
        return sd.get_stream() is not None 