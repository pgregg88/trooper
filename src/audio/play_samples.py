"""Play processed voice samples.

This script plays the processed Stormtrooper voice samples.
"""

import sys
import time
from pathlib import Path
from typing import List
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.audio import AudioPlayer, AudioError

def get_processed_files() -> List[Path]:
    """Get list of processed audio files.
    
    Returns:
        List[Path]: List of paths to processed audio files
    """
    processed_dir = project_root / "assets" / "audio" / "processed"
    
    if not processed_dir.exists():
        raise RuntimeError("Processed audio directory not found. Please run process_samples.py first.")
    
    return sorted(processed_dir.glob("*.wav"))

def play_sample(player: AudioPlayer, file_path: Path) -> bool:
    """Play a processed audio sample.
    
    Args:
        player: Audio player instance
        file_path: Path to audio file
        
    Returns:
        bool: True to continue, False to quit
    """
    try:
        logger.info(f"\nPlaying: {file_path.name}")
        player.play_file(str(file_path))
        
        response = input("\nPress Enter to continue to next sample, or 'q' to quit: ")
        return response.lower() != 'q'
        
    except (AudioError, IOError) as e:
        logger.error(f"Error playing {file_path.name}: {str(e)}")
        return True

def main() -> None:
    """Play processed audio samples."""
    try:
        player = AudioPlayer()
        files = get_processed_files()
        
        if not files:
            logger.error("No processed samples found")
            return
            
        logger.info(f"Found {len(files)} processed samples to play")
        
        for file_path in files:
            if not play_sample(player, file_path):
                break
                
    except (AudioError, RuntimeError) as e:
        logger.error(f"Playback error: {str(e)}")

if __name__ == "__main__":
    main() 