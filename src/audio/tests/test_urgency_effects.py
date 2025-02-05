"""Test script for urgency-based audio effects."""

import sys
from pathlib import Path
from typing import Optional
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.quotes import QuoteManager, UrgencyLevel
from src.audio import StormtrooperEffect, EffectParams

def test_urgency_effects():
    """Test audio processing with different urgency levels."""
    # Initialize quote manager and effect processor
    quotes_file = project_root / "config" / "quotes.yaml"
    manager = QuoteManager(quotes_file)
    effect = StormtrooperEffect()
    
    # Process a quote from each urgency level
    for urgency in [UrgencyLevel.LOW, UrgencyLevel.MEDIUM, UrgencyLevel.HIGH]:
        logger.info(f"\nTesting {urgency.value} urgency effects:")
        
        # Get a random quote with this urgency
        quote = manager.get_random_quote(urgency=urgency.value)
        if not quote:
            logger.warning(f"No quotes found with urgency {urgency.value}")
            continue
            
        logger.info(f"Selected quote: {quote.text}")
        logger.info(f"Category: {quote.category.value}")
        logger.info(f"Context: {quote.context}")
        logger.info(f"Tags: {quote.tags}")
        
        # Find the most recent processed file for this quote
        input_files = list(project_root.glob(f"assets/audio/polly_raw/*{quote.category.value}*.wav"))
        if not input_files:
            logger.warning("No matching audio files found")
            continue
            
        input_file = input_files[0]  # Use first matching file
        logger.info(f"Processing file: {input_file.name}")
        
        # Process with urgency-based effects
        effect.process_file(
            input_file,
            urgency=urgency
        )

if __name__ == "__main__":
    test_urgency_effects() 