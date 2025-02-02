"""Process audio samples with Stormtrooper voice effects.

This script processes audio files from the polly_raw directory and saves
the processed versions in the processed directory. Input files can be MP3 or WAV,
but processing is done in WAV format for better quality.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.audio import StormtrooperEffect, EffectParams

def setup_directories() -> Tuple[Path, Path]:
    """Create and verify required directories exist.
    
    Returns:
        Tuple[Path, Path]: Paths to input and output directories
    """
    input_dir = project_root / "assets" / "audio" / "polly_raw"
    output_dir = project_root / "assets" / "audio" / "processed"
    
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return input_dir, output_dir

def get_input_files(input_dir: Path) -> List[Path]:
    """Get list of input files to process.
    
    Args:
        input_dir: Directory containing input files
        
    Returns:
        List of paths to process
    """
    # Support both MP3 and WAV files
    mp3_files = list(input_dir.glob("*.mp3"))
    wav_files = list(input_dir.glob("*.wav"))
    return sorted(mp3_files + wav_files)

def process_samples():
    """Process all audio samples with Stormtrooper effects."""
    # Initialize effect processor with WAV output
    params = EffectParams(output_format="WAV")
    effect = StormtrooperEffect(params)
    
    # Setup directories
    input_dir, output_dir = setup_directories()
    
    # Get input files
    input_files = get_input_files(input_dir)
    logger.info(f"Found {len(input_files)} samples to process")
    
    # Process each file
    for input_file in input_files:
        try:
            # Always use .wav extension for processed files
            output_file = output_dir / f"{input_file.stem}_processed.wav"
            
            # Skip if output exists and is newer than input
            if output_file.exists() and output_file.stat().st_mtime > input_file.stat().st_mtime:
                logger.info(f"Skipping {input_file.name} - already processed")
                continue
                
            logger.info(f"Processing: {input_file.name}")
            effect.process_file(str(input_file), str(output_file))
            
        except Exception as e:
            logger.error(f"Failed to process {input_file.name}: {str(e)}")
            continue

if __name__ == "__main__":
    process_samples() 