"""Test audio playback."""
import time
from pathlib import Path
from loguru import logger
from .player import AudioPlayer

def test_playback():
    """Test audio playback with USB device."""
    player = AudioPlayer()
    
    # Test with a simple audio file
    test_file = Path("assets/audio/polly_raw/Matthew_neural_spotted_patrol_001_stop_right_there_processed.wav")
    
    if not test_file.exists():
        logger.error(f"Test file not found: {test_file}")
        return
        
    logger.info("Testing audio playback...")
    success = player.play_file(str(test_file))
    
    if success:
        logger.info("Audio playback successful!")
    else:
        logger.error("Audio playback failed!")

if __name__ == "__main__":
    test_playback() 