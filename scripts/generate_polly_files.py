"""Script to generate missing audio files using AWS Polly."""

import sys
from pathlib import Path
from typing import Dict, List
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.quotes import QuoteManager, Quote
from src.audio.polly import PollyClient
from src.audio.utils import generate_filename

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
    
    logger.info(f"Generating {total_quotes} audio files...")
    
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
                # Generate audio with Polly
                logger.info(f"Generating audio for: {quote.text}")
                polly.generate_speech(quote.text, str(output_path))
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