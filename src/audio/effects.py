"""Audio effects processing for Stormtrooper voice."""

from pathlib import Path
from typing import Optional, Union, Tuple
from dataclasses import dataclass
import random
from loguru import logger
import numpy as np
from scipy import signal
import soundfile as sf

from src.quotes import UrgencyLevel, URGENCY_EFFECTS

@dataclass
class EffectParams:
    """Parameters for Stormtrooper voice effects."""
    
    # Audio Format
    sample_rate: int = 44100
    output_format: str = "WAV"
    
    # Filter Curve EQ
    highpass_freq: float = 500.0  # Hz
    lowpass_freq: float = 2000.0  # Hz
    mid_boost_db: float = 8.0     # dB boost in passband
    filter_order: int = 4
    
    # Radio Effects - These are base values, modified by urgency
    static_duration_min: float = 0.03  # Duration of static in seconds
    static_duration_max: float = 0.1   # Duration of static in seconds
    static_volume: float = 0.1    # Volume of static (0-1)
    static_variation: float = 0.5  # Random variation in static volume
    
    # Mic Click
    click_duration: float = 0.02   # Duration of click in seconds
    click_volume: float = 0.15     # Volume of click (0-1)
    click_freq: float = 2000.0     # Frequency of click sound (Hz)
    click_variation: float = 0.3   # Random variation in click parameters

class StormtrooperEffect:
    """Audio effects processor for Stormtrooper voice."""
    
    def __init__(self, params: Optional[EffectParams] = None):
        """Initialize the effects processor.
        
        Args:
            params: Optional effect parameters
        """
        self.params = params or EffectParams()
        self.sample_rate = self.params.sample_rate
        self.current_urgency = UrgencyLevel.MEDIUM  # Default urgency
        logger.info("Initialized Stormtrooper effects processor")
        
    def set_urgency(self, urgency: Union[UrgencyLevel, str]) -> None:
        """Set the urgency level for effect parameters.
        
        Args:
            urgency: Urgency level to use for effects
        """
        if isinstance(urgency, str):
            urgency = UrgencyLevel(urgency)
        self.current_urgency = urgency
        logger.debug(f"Set effect urgency to: {urgency.value}")
        
    def _get_urgency_params(self) -> dict:
        """Get effect parameters for current urgency level.
        
        Returns:
            Dictionary of effect parameters
        """
        return URGENCY_EFFECTS[self.current_urgency.value]
        
    def process_file(self, input_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None, urgency: Optional[Union[UrgencyLevel, str]] = None) -> str:
        """Process an audio file with Stormtrooper effects.
        
        Args:
            input_path: Path to input audio file (MP3 or WAV)
            output_path: Optional path for output file. If not provided,
                        will append '_processed' to input filename
            urgency: Optional urgency level for effects
            
        Returns:
            Path to processed audio file
        """
        if urgency:
            self.set_urgency(urgency)
            
        try:
            # Convert paths to Path objects
            input_path = Path(input_path)
            
            # Read audio file
            data, sample_rate = sf.read(str(input_path))
            self.sample_rate = sample_rate
            
            # Convert to mono if stereo
            if len(data.shape) > 1:
                data = np.mean(data, axis=1)
            
            # Process audio
            processed = self._process_audio(data)
            
            # Generate output path if not provided
            if output_path is None:
                output_path = input_path.parent / f"{input_path.stem}_processed.wav"
            else:
                output_path = Path(output_path)
                if output_path.suffix.lower() not in ['.wav', '.mp3']:
                    output_path = output_path.with_suffix('.wav')
            
            # Save processed audio
            sf.write(str(output_path), processed, sample_rate, format='WAV', subtype='PCM_16')
            logger.info(f"Saved processed audio to: {output_path}")
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Failed to process audio file: {str(e)}")
            raise
            
    def _process_audio(self, data: np.ndarray) -> np.ndarray:
        """Apply Stormtrooper effects to audio data.
        
        Args:
            data: Input audio data
            
        Returns:
            Processed audio data
        """
        # Normalize input
        data = data / np.max(np.abs(data))
        
        # Apply Filter Curve EQ
        data = self._apply_filter_curve_eq(data)
        
        # Add radio effects
        data = self._add_radio_effects(data)
        
        # Final normalization and clipping
        data = data / np.max(np.abs(data))
        data = np.clip(data, -1.0, 1.0)
        
        return data
        
    def _apply_filter_curve_eq(self, data: np.ndarray) -> np.ndarray:
        """Apply Filter Curve EQ with mid-frequency boost.
        
        Args:
            data: Input audio data
            
        Returns:
            Filtered audio data with mid boost
        """
        nyquist = self.sample_rate / 2
        
        # Design bandpass filter
        low = self.params.highpass_freq / nyquist
        high = self.params.lowpass_freq / nyquist
        b, a = signal.butter(self.params.filter_order, [low, high], btype='band')
        
        # Apply bandpass filter
        filtered = signal.filtfilt(b, a, data)
        
        # Apply mid-frequency boost
        boost_factor = 10 ** (self.params.mid_boost_db / 20)  # Convert dB to linear gain
        filtered *= boost_factor
        
        return filtered
        
    def _add_radio_effects(self, data: np.ndarray) -> np.ndarray:
        """Add radio static and mic click effects at start and end.
        
        Args:
            data: Input audio data
            
        Returns:
            Audio data with radio effects
        """
        # Get urgency-based parameters
        urgency_params = self._get_urgency_params()
        
        # Calculate random static duration and samples for effects
        static_duration = random.uniform(
            urgency_params["static_duration_min"],
            urgency_params["static_duration_max"]
        )
        static_samples = int(static_duration * self.sample_rate)
        click_samples = int(self.params.click_duration * self.sample_rate)
        
        # Generate start mic click with urgency-based volume
        start_click_volume = urgency_params["click_volume"] * (
            1 + random.uniform(
                -urgency_params["click_variation"],
                urgency_params["click_variation"]
            )
        )
        start_click_freq = self.params.click_freq * (1 + random.uniform(-self.params.click_variation, self.params.click_variation))
        t = np.linspace(0, self.params.click_duration, click_samples)
        start_click = start_click_volume * np.sin(2 * np.pi * start_click_freq * t) * np.exp(-t / (self.params.click_duration * 0.2))
        
        # Generate end mic click with different variation
        end_click_volume = urgency_params["click_volume"] * (
            1 + random.uniform(
                -urgency_params["click_variation"],
                urgency_params["click_variation"]
            )
        )
        end_click_freq = self.params.click_freq * (1 + random.uniform(-self.params.click_variation, self.params.click_variation))
        end_click = end_click_volume * np.sin(2 * np.pi * end_click_freq * t) * np.exp(-t / (self.params.click_duration * 0.2))
        
        # Generate static with urgency-based volume
        static_volume = urgency_params["static_volume"] * (
            1 + random.uniform(
                -urgency_params["static_variation"],
                urgency_params["static_variation"]
            )
        )
        static = np.random.normal(0, static_volume, static_samples)
        
        # Create output buffer with space for start click, audio, end click, and static
        total_length = click_samples + len(data) + click_samples + static_samples
        result = np.zeros(total_length)
        
        # Add effects in sequence
        result[:click_samples] = start_click                          # Start click
        result[click_samples:click_samples + len(data)] = data       # Main audio
        pos = click_samples + len(data)
        result[pos:pos + click_samples] = end_click                  # End click
        result[pos + click_samples:] = static                        # Static at the very end
        
        return result 