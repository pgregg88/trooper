"""Response generator for Stormtrooper voice responses."""

import random
from typing import List, Optional
from loguru import logger

class ResponseGenerator:
    """Generate contextual Stormtrooper responses."""
    
    def __init__(self):
        """Initialize response generator."""
        # Default responses for different contexts
        self.greetings = [
            "Move along, citizen.",
            "Nothing to see here.",
            "Imperial business. Move along.",
            "Identification, please.",
        ]
        
        self.alerts = [
            "Stop right there!",
            "Halt! In the name of the Empire!",
            "Freeze! Don't move!",
            "You there! Stop!",
        ]
        
        self.confirmations = [
            "Copy that.",
            "Understood.",
            "Affirmative.",
            "Roger that.",
        ]
        
        self.denials = [
            "Negative.",
            "That's a negative.",
            "Access denied.",
            "Not authorized.",
        ]
        
        logger.info("Initialized response generator")
    
    def get_greeting(self) -> str:
        """Get a random greeting response."""
        response = random.choice(self.greetings)
        logger.debug(f"Generated greeting: {response}")
        return response
    
    def get_alert(self) -> str:
        """Get a random alert response."""
        response = random.choice(self.alerts)
        logger.debug(f"Generated alert: {response}")
        return response
    
    def get_confirmation(self) -> str:
        """Get a random confirmation response."""
        response = random.choice(self.confirmations)
        logger.debug(f"Generated confirmation: {response}")
        return response
    
    def get_denial(self) -> str:
        """Get a random denial response."""
        response = random.choice(self.denials)
        logger.debug(f"Generated denial: {response}")
        return response
    
    def add_response(self, category: str, response: str):
        """Add a new response to a category.
        
        Args:
            category: Response category (greetings, alerts, etc.)
            response: New response to add
        """
        if hasattr(self, category):
            getattr(self, category).append(response)
            logger.info(f"Added new {category} response: {response}")
        else:
            logger.error(f"Invalid response category: {category}")
    
    def get_random_response(self) -> str:
        """Get a random response from any category."""
        all_responses = (
            self.greetings +
            self.alerts +
            self.confirmations +
            self.denials
        )
        response = random.choice(all_responses)
        logger.debug(f"Generated random response: {response}")
        return response 