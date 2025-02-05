#!/usr/bin/env python3
"""Script to generate processed Stormtrooper voice files from quotes."""

import sys
import argparse
from pathlib import Path
from typing import Optional
import numpy as np
import soundfile as sf
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.quotes import QuoteManager
from src.audio.polly import PollyClient
from src.audio.effects import StormtrooperEffect, EffectParams

def setup_directories(clean: bool = False) -> tuple[Path, Path]:
    """Create and verify required directories exist.
    
    Args:
        clean: If True, delete all existing files in the directories
    
    Returns:
        Tuple of (polly_raw_dir, processed_dir)
    """
    polly_raw_dir = project_root / "assets" / "audio" / "polly_raw"
    processed_dir = project_root / "assets" / "audio" / "processed"
    
    # Clean existing files if requested
    if clean:
        if polly_raw_dir.exists():
            logger.info("Cleaning polly_raw directory...")
            for file in polly_raw_dir.glob("*.wav"):
                file.unlink()
        if processed_dir.exists():
            logger.info("Cleaning processed directory...")
            for file in processed_dir.glob("*.wav"):
                file.unlink()
    
    polly_raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    return polly_raw_dir, processed_dir

def generate_processed_quotes(quotes_file: Optional[Path] = None, clean: bool = False) -> None:
    """Generate processed audio files for all quotes.
    
    Args:
        quotes_file: Optional path to quotes YAML file. If not provided,
                    uses default config/quotes.yaml
        clean: If True, delete all existing files before processing
    """
    # Setup
    quotes_file = quotes_file or (project_root / "config" / "quotes.yaml")
    polly_raw_dir, processed_dir = setup_directories(clean)
    
    # Initialize components
    quote_manager = QuoteManager(quotes_file)
    polly = PollyClient()
    effect = StormtrooperEffect()
    
    total_quotes = len(quote_manager.quotes)
    generated = 0
    skipped = 0
    failed = 0
    
    logger.info(f"Processing {total_quotes} quotes...")
    
    # Process each quote
    for quote in quote_manager.quotes:
        try:
            # Generate filename base (without extension)
            # Clean text for filename (first few words)
            clean_text = "_".join(quote.text.split()[:3]).lower()
            clean_text = "".join(c for c in clean_text if c.isalnum() or c == "_")
            
            base_name = f"Matthew_neural_{quote.category.value}_{quote.context}_{clean_text}"
            raw_path = polly_raw_dir / f"{base_name}.wav"
            processed_path = processed_dir / f"{base_name}_processed.wav"
            
            # Skip if processed file exists and is newer than raw file
            if processed_path.exists():
                if not raw_path.exists() or processed_path.stat().st_mtime > raw_path.stat().st_mtime:
                    logger.debug(f"Skipping {base_name} - already processed")
                    skipped += 1
                    continue
            
            # Generate raw audio if needed
            if not raw_path.exists():
                logger.info(f"Generating audio for: {quote.text}")
                pcm_data = polly.generate_speech(
                    text=quote.text,
                    urgency=quote.urgency.value,
                    context=quote.context
                )
                
                # Ensure we have bytes data
                if isinstance(pcm_data, str):
                    logger.error(f"Unexpected string return from Polly for {quote.text}")
                    failed += 1
                    continue
                
                # Convert PCM bytes to float32 array
                audio_data = np.frombuffer(pcm_data, dtype=np.int16)
                audio_float = audio_data.astype(np.float32) / 32768.0
                
                # Save as WAV
                sf.write(str(raw_path), audio_float, 16000, format='WAV', subtype='FLOAT')
            
            # Apply effects
            logger.info(f"Applying effects to: {raw_path.name}")
            effect.process_file(
                str(raw_path),
                str(processed_path),
                urgency=quote.urgency
            )
            
            generated += 1
            
        except Exception as e:
            logger.error(f"Failed to process quote: {quote.text}")
            logger.error(f"Error: {str(e)}")
            failed += 1
            continue
    
    # Summary
    logger.info("\nProcessing complete:")
    logger.info(f"Total quotes: {total_quotes}")
    logger.info(f"Generated: {generated}")
    logger.info(f"Skipped: {skipped}")
    logger.info(f"Failed: {failed}")

def main():
    """Run the quote processing pipeline."""
    parser = argparse.ArgumentParser(description="Generate processed Stormtrooper voice files from quotes.")
    parser.add_argument("--clean", action="store_true", help="Delete existing files before processing")
    parser.add_argument("--quotes-file", type=Path, help="Path to quotes YAML file (default: config/quotes.yaml)")
    
    args = parser.parse_args()
    
    generate_processed_quotes(
        quotes_file=args.quotes_file,
        clean=args.clean
    )

if __name__ == "__main__":
    main() 