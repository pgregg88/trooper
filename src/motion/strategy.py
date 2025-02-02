"""Motion response selection strategy."""

import random
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
import time
import yaml
from loguru import logger

from .constants import MotionDirection

@dataclass
class ResponseParams:
    """Parameters for quote selection."""
    category: str
    context: str
    tags: List[str]
    urgency: str

class ResponseStrategy:
    """Strategy for selecting appropriate responses to motion."""
    
    def __init__(self, config_path: Path):
        """Initialize the response strategy.
        
        Args:
            config_path: Path to motion response configuration file
        """
        self.config = self._load_config(config_path)
        self.last_used_times: Dict[str, float] = {}  # Track when quotes were last used
        
    def _load_config(self, config_path: Path) -> Dict:
        """Load motion response configuration.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Loaded configuration dictionary
        """
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded motion response config from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Failed to load motion response config: {str(e)}")
            raise
            
    def _get_direction_config(self, direction: MotionDirection) -> Dict:
        """Get configuration for a specific direction.
        
        Args:
            direction: Motion direction
            
        Returns:
            Direction-specific configuration
        """
        return self.config['directions'][direction]
        
    def _weighted_choice(self, options: List[str], weights: Dict[str, float]) -> str:
        """Make a weighted random choice from options.
        
        Args:
            options: List of options to choose from
            weights: Dictionary of weights for each option
            
        Returns:
            Selected option
        """
        # Filter weights to only include available options
        valid_weights = {k: v for k, v in weights.items() if k in options}
        
        if not valid_weights:
            # If no weights available, use uniform distribution
            return random.choice(options)
            
        # Normalize weights
        total = sum(valid_weights.values())
        normalized = {k: v/total for k, v in valid_weights.items()}
        
        # Make weighted choice
        r = random.random()
        cumsum = 0
        for option, weight in normalized.items():
            cumsum += weight
            if r <= cumsum:
                return option
                
        # Fallback (shouldn't happen due to normalization)
        return random.choice(options)
        
    def select_quote_params(self, direction: MotionDirection) -> ResponseParams:
        """Select parameters for quote selection based on motion direction.
        
        Args:
            direction: Direction motion was detected from
            
        Returns:
            Selected response parameters
        """
        dir_config = self._get_direction_config(direction)
        settings = self.config['settings']
        
        # Get available options and weights
        categories = dir_config['categories']
        contexts = dir_config['contexts']
        tags = dir_config['tags']
        urgency_levels = dir_config['urgency_levels']
        
        # Get weights (direction-specific or default)
        dir_weights = dir_config.get('weights', {})
        def_weights = settings['default_weights']
        
        # Make weighted selections
        category = self._weighted_choice(
            categories,
            dir_weights.get('categories', def_weights['categories'])
        )
        
        context = self._weighted_choice(
            contexts,
            dir_weights.get('contexts', def_weights['contexts'])
        )
        
        urgency = self._weighted_choice(
            urgency_levels,
            dir_weights.get('urgency', def_weights['urgency'])
        )
        
        # For tags, we select a random subset based on weights
        selected_tags = []
        tag_weights = dir_weights.get('tags', def_weights['tags'])
        for tag in tags:
            if tag in tag_weights:
                if random.random() < tag_weights[tag]:
                    selected_tags.append(tag)
                    
        if not selected_tags:  # Ensure at least one tag
            selected_tags = [random.choice(tags)]
            
        return ResponseParams(
            category=category,
            context=context,
            tags=selected_tags,
            urgency=urgency
        ) 