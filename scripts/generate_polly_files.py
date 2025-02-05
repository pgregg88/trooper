"""Script to generate missing audio files using AWS Polly."""

import sys
from pathlib import Path
from typing import Dict, List
import numpy as np
import numpy.typing as npt
from scipy import signal
import soundfile as sf
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.quotes import QuoteManager, Quote
from src.audio.polly import PollyClient
from src.audio.utils import generate_filename

def resample_to_44100(data: bytes, src_rate: int = 16000) -> npt.NDArray[np.float32]:
    """Resample PCM audio data to 44.1kHz.
    
    Args:
        data: Raw PCM audio data
        src_rate: Source sample rate
        
    Returns:
        Resampled audio data as float32 array normalized between -1 and 1
    """
    # Ensure data length is multiple of 2 (int16)
    if len(data) % 2 != 0:
        data = data[:-1]
        logger.warning("Trimmed odd byte from PCM data")
    
    # Convert PCM bytes to float32 array
    samples = np.frombuffer(data, dtype=np.int16)
    audio = samples.astype(np.float32) / 32768.0
    
    # Calculate resampling parameters
    src_samples = len(audio)
    dst_rate = 44100
    dst_samples = int(src_samples * float(dst_rate) / float(src_rate))
    
    # Resample audio
    resampled = np.array(signal.resample(audio, dst_samples), dtype=np.float32)
    
    return resampled

def generate_polly_files(quotes_file: Path, output_dir: Path) -> None:
    """Generate missing audio files using AWS Polly.
    
    Args:
        quotes_file: Path to quotes YAML file
        output_dir: Directory to save audio files
    """
    # Initialize components
    quote_manager = QuoteManager(quotes_file)
    polly = PollyClient()
    
    # Group quotes by category and context
    quote_groups = {}
    for quote in quote_manager.quotes:
        key = (quote.category.value, quote.context)
        if key not in quote_groups:
            quote_groups[key] = []
        quote_groups[key].append(quote)
    
    # Generate audio for each quote
    total_quotes = len(quote_manager.quotes)
    generated = 0
    skipped = 0
    
    logger.info(f"Generating {total_quotes} audio files at 44.1kHz...")
    
    for _, quotes in quote_groups.items():
        for i, quote in enumerate(quotes):
            # Generate filename
            filename = generate_filename("Matthew", quote, i)
            output_path = output_dir / filename
            
            # Skip if file exists
            if output_path.exists():
                logger.debug(f"Skipping existing file: {filename}")
                skipped += 1
                continue
            
            try:
                # Generate audio with Polly at 16kHz
                logger.info(f"Generating audio for: {quote.text}")
                pcm_data = polly.generate_speech(quote.text)
                
                # Ensure we got bytes and not a file path
                if isinstance(pcm_data, str):
                    logger.error(f"Unexpected string return from Polly for {filename}")
                    continue
                
                # Resample to 44.1kHz
                resampled_data = resample_to_44100(pcm_data)
                
                # Save as WAV
                sf.write(str(output_path), resampled_data, 44100, format='WAV', subtype='PCM_16')
                generated += 1
                
            except Exception as e:
                logger.error(f"Failed to generate audio for {filename}: {str(e)}")
    
    logger.info("Audio generation complete:")
    logger.info(f"- Total quotes: {total_quotes}")
    logger.info(f"- Generated: {generated}")
    logger.info(f"- Skipped (existing): {skipped}")
    logger.info(f"- Failed: {total_quotes - generated - skipped}")

def main():
    """Run the Polly file generation script."""
    quotes_file = project_root / "config" / "quotes.yaml"
    output_dir = project_root / "assets" / "audio" / "polly_raw"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate audio files
    generate_polly_files(quotes_file, output_dir)

if __name__ == "__main__":
    main() 