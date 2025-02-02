"""Audio effects configuration for Stormtrooper voice."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class AudioEffectsConfig:
    """Audio effects configuration."""
    
    # Bandpass filter settings
    bandpass_low: int = 300
    bandpass_high: int = 3000
    
    # Radio distortion settings
    distortion_amount: float = 0.5
    noise_level: float = 0.1
    
    # Echo/reverb settings
    echo_delay: float = 0.08  # 80ms
    echo_decay: float = 0.5
    
    # Output settings
    output_gain: float = 1.0
    
    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "bandpass": {
                "low": self.bandpass_low,
                "high": self.bandpass_high,
            },
            "distortion": {
                "amount": self.distortion_amount,
                "noise": self.noise_level,
            },
            "echo": {
                "delay": self.echo_delay,
                "decay": self.echo_decay,
            },
            "output": {
                "gain": self.output_gain,
            },
        } 