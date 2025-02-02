"""Motion detection and response handling."""

from pathlib import Path
from typing import Optional, List
import random
import re
from loguru import logger

from src.quotes import QuoteManager, QuoteCategory, UrgencyLevel, Quote
from src.audio import StormtrooperEffect, AudioPlayer
from .strategy import ResponseStrategy
from .types import MotionDirection

class MotionHandler:
    """Handler for motion detection and response."""
    
    def __init__(
        self,
        quotes_file: Optional[Path] = None,
        config_file: Optional[Path] = None
    ):
        """Initialize the motion handler.
        
        Args:
            quotes_file: Optional path to quotes YAML file
            config_file: Optional path to motion response config file
        """
        # Set default paths if not provided
        if quotes_file is None:
            quotes_file = Path("config/quotes.yaml")
        if config_file is None:
            config_file = Path("config/motion_responses.yaml")
            
        # Initialize components
        self.quote_manager = QuoteManager(quotes_file)
        self.response_strategy = ResponseStrategy(config_file)
        self.player = AudioPlayer()
        
        # Track state
        self.is_responding = False
        self.last_direction: Optional[MotionDirection] = None
        
    def _text_to_filename(self, text: str) -> str:
        """Convert quote text to a filename-safe format.
        
        Args:
            text: Quote text to convert
            
        Returns:
            Filename-safe version of the text
        """
        # Remove punctuation and convert to lowercase
        safe = re.sub(r'[^\w\s-]', '', text.lower())
        # Replace spaces with underscores and limit length
        return '_'.join(safe.split())[:30]
        
    def _find_matching_audio(self, quote: Quote) -> Optional[Path]:
        """Find the best matching audio file for a quote.
        
        Args:
            quote: Quote to find audio for
            
        Returns:
            Path to best matching audio file, or None if no match found
        """
        audio_dir = Path("assets/audio/polly_raw")
        
        # Convert quote text to filename format
        safe_text = self._text_to_filename(quote.text)
        
        # Try increasingly lenient patterns
        patterns = [
            # Try exact match with processed suffix
            f"*{quote.category.value}_{quote.context}*{safe_text}*_processed.wav",
            # Try partial text match
            f"*{quote.category.value}_{quote.context}*{safe_text[:15]}*_processed.wav",
            # Try just category and context
            f"*{quote.category.value}_{quote.context}*_processed.wav",
            # Fallback to just category
            f"*{quote.category.value}*_processed.wav"
        ]
        
        for pattern in patterns:
            matches = list(audio_dir.glob(pattern))
            if matches:
                # Log which pattern matched
                logger.debug(f"Found audio match using pattern: {pattern}")
                return random.choice(matches)
                
        return None
        
    def handle_motion(self, direction: MotionDirection) -> None:
        """Handle detected motion and play appropriate response.
        
        Args:
            direction: Direction motion was detected from
        """
        if self.is_responding:
            logger.debug("Already responding to motion, ignoring new detection")
            return
            
        try:
            self.is_responding = True
            self.last_direction = direction
            
            # Get response parameters from strategy
            params = self.response_strategy.select_quote_params(direction)
            
            # Try to get quote with current parameters
            quote = self.quote_manager.get_random_quote(
                category=params.category,
                context=params.context,
                urgency=params.urgency,
                tags=params.tags,
                exclude_recent=True
            )
            
            # If no quote found, try fallback options
            if not quote:
                # Try without context restriction
                quote = self.quote_manager.get_random_quote(
                    category=params.category,
                    urgency=params.urgency,
                    tags=params.tags,
                    exclude_recent=True
                )
                
                # If still no quote, try with just category
                if not quote:
                    quote = self.quote_manager.get_random_quote(
                        category=params.category,
                        exclude_recent=True
                    )
            
            if not quote:
                logger.warning(f"No appropriate response found for motion from {direction}")
                return
                
            logger.info(f"Selected response: {quote.text}")
            
            # Find best matching audio file
            audio_file = self._find_matching_audio(quote)
            if not audio_file:
                logger.error(f"No matching audio file found for quote: {quote.text}")
                return
                
            # Play the audio
            logger.debug(f"Playing audio file: {audio_file.name}")
            self.player.play_file(str(audio_file))
            
        finally:
            self.is_responding = False 