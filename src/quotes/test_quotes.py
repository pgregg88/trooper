"""Test script for quote management system."""

import sys
from pathlib import Path
from typing import Optional
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.quotes import QuoteManager, QuoteCategory, UrgencyLevel

def test_quote_selection():
    """Test quote selection with various criteria."""
    quotes_file = project_root / "config" / "quotes.yaml"
    manager = QuoteManager(quotes_file)
    
    # Test getting quotes by category
    logger.info("\nTesting category filter (spotted):")
    spotted_quotes = manager.get_quotes(category="spotted")
    logger.info(f"Found {len(spotted_quotes)} spotted quotes")
    
    # Test getting quotes by context
    logger.info("\nTesting context filter (combat):")
    combat_quotes = manager.get_quotes(context="combat")
    logger.info(f"Found {len(combat_quotes)} combat quotes")
    
    # Test getting quotes by urgency
    logger.info("\nTesting urgency filter (high):")
    high_urgency = manager.get_quotes(urgency="high")
    logger.info(f"Found {len(high_urgency)} high urgency quotes")
    
    # Test getting quotes by tags
    logger.info("\nTesting tag filter (jedi):")
    jedi_quotes = manager.get_quotes(tags=["jedi"])
    logger.info(f"Found {len(jedi_quotes)} Jedi-related quotes")
    
    # Test random quote selection
    logger.info("\nTesting random quote selection:")
    for _ in range(3):
        quote = manager.get_random_quote(category="spotted", urgency="high")
        if quote:
            logger.info(f"Random quote: {quote.text}")
            logger.info(f"Category: {quote.category.value}")
            logger.info(f"Context: {quote.context}")
            logger.info(f"Urgency: {quote.urgency.value}")
            logger.info(f"Tags: {quote.tags}\n")

if __name__ == "__main__":
    test_quote_selection() 