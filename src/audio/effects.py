"""Audio effects processing for Stormtrooper voice."""

import numpy as np
from typing import Optional, Union
from pathlib import Path
import soundfile as sf
from loguru import logger
from config.audio_effects import AudioEffectsConfig

class AudioEffects:
    """Audio effects processor for Stormtrooper voice."""
    
    def __init__(self, config: Optional[AudioEffectsConfig] = None):
        """Initialize audio effects processor.
        
        Args:
            config: Optional audio effects configuration
        """
        self.config = config or AudioEffectsConfig()
        logger.info("Initialized audio effects processor")
    
    def process_file(self, input_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None) -> str:
        """Process an audio file with Stormtrooper effects.
        
        Args:
            input_path: Path to input audio file
            output_path: Optional path for output file. If not provided,
                        will append '_processed' to input filename
        
        Returns:
            Path to processed audio file as string
        """
        try:
            # Convert paths to Path objects
            input_path_obj = Path(input_path)
            
            # Read audio file
            data, samplerate = sf.read(str(input_path_obj))
            
            # Apply effects
            processed = self._apply_effects(data)
            
            # Generate output path if not provided
            if output_path is None:
                output_path = str(input_path_obj.parent / f"{input_path_obj.stem}_processed{input_path_obj.suffix}")
            else:
                output_path = str(Path(output_path))
            
            # Save processed audio
            sf.write(output_path, processed, samplerate)
            logger.info(f"Processed audio saved to: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to process audio file: {str(e)}")
            raise
    
    def _apply_effects(self, data: np.ndarray) -> np.ndarray:
        """Apply audio effects to numpy array of audio data.
        
        Args:
            data: Input audio data
            
        Returns:
            Processed audio data
        """
        # Apply bandpass filter
        data = self._bandpass_filter(data)
        
        # Add radio distortion
        data = self._add_distortion(data)
        
        # Add echo effect
        data = self._add_echo(data)
        
        # Apply output gain
        data *= self.config.output_gain
        
        # Clip to prevent distortion
        data = np.clip(data, -1.0, 1.0)
        
        return data
    
    def _bandpass_filter(self, data: np.ndarray) -> np.ndarray:
        """Apply bandpass filter to simulate radio communication."""
        # TODO: Implement proper bandpass filter
        return data
    
    def _add_distortion(self, data: np.ndarray) -> np.ndarray:
        """Add radio-like distortion and noise."""
        # Add noise
        noise = np.random.normal(0, self.config.noise_level, data.shape)
        data = data + noise
        
        # Add distortion
        data = np.clip(data * (1 + self.config.distortion_amount), -1.0, 1.0)
        
        return data
    
    def _add_echo(self, data: np.ndarray) -> np.ndarray:
        """Add echo/reverb effect."""
        # Calculate delay in samples
        delay_samples = int(self.config.echo_delay * 44100)  # Use standard sample rate
        
        # Create delayed signal
        delayed = np.zeros_like(data)
        delayed[delay_samples:] = data[:-delay_samples] * self.config.echo_decay
        
        # Mix original and delayed signals
        return data + delayed 