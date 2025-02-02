"""Global settings for Stormtrooper Voice Assistant."""

from pathlib import Path
from typing import Dict, Any
from loguru import logger

class Settings:
    """Global settings configuration."""
    
    def __init__(self):
        """Initialize settings."""
        # Project paths
        self.project_root = Path(__file__).parent.parent
        self.src_dir = self.project_root / "src"
        self.assets_dir = self.project_root / "assets"
        self.audio_cache_dir = self.assets_dir / "audio" / "cache"
        self.audio_responses_dir = self.assets_dir / "audio" / "responses"
        
        # AWS settings
        self.aws_profile = "trooper"
        self.aws_region = "us-east-1"
        
        # Audio settings
        self.sample_rate = 44100
        self.channels = 1
        
        # Create directories
        self._create_directories()
        
        logger.info("Settings initialized")
    
    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            self.audio_cache_dir,
            self.audio_responses_dir,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        return {
            "project_root": str(self.project_root),
            "src_dir": str(self.src_dir),
            "assets_dir": str(self.assets_dir),
            "audio_cache_dir": str(self.audio_cache_dir),
            "audio_responses_dir": str(self.audio_responses_dir),
            "aws_profile": self.aws_profile,
            "aws_region": self.aws_region,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
        } 