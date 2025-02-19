"""Audio playback functionality."""

import platform
from typing import Optional, Dict, Any, Union, cast, TypedDict
import numpy as np
from scipy import signal
import sounddevice as sd
import soundfile as sf
from loguru import logger

class DeviceInfo(TypedDict, total=False):
    """Type definition for sounddevice device info."""
    name: str
    max_output_channels: int
    default_samplerate: float

class AudioPlayer:
    """Audio playback handler."""
    
    # Common sample rates supported by most devices
    # 44.1kHz is the preferred rate for best quality and compatibility
    SUPPORTED_RATES = [44100, 48000, 22050, 16000]
    DEFAULT_RATE = 44100  # CD-quality audio
    
    # Volume settings
    MIN_VOLUME = 1
    MAX_VOLUME = 11
    DEFAULT_VOLUME = 5
    
    def __init__(self):
        """Initialize the audio player."""
        self.system = platform.system()
        self.volume = self.DEFAULT_VOLUME
        self._configure_device()
        logger.info(f"Initialized audio player on {self.system}")
        
    def set_volume(self, volume: float) -> None:
        """Set playback volume level.
        
        Args:
            volume: Volume level from 1 (quietest) to 11 (loudest)
        """
        self.volume = max(self.MIN_VOLUME, min(self.MAX_VOLUME, volume))
        logger.info(f"Volume set to: {self.volume}")
        
    def get_volume(self) -> float:
        """Get current volume level.
        
        Returns:
            Current volume level (1-11)
        """
        return self.volume
        
    def _configure_device(self) -> None:
        """Configure audio device based on platform."""
        try:
            if self.system == 'Darwin':  # macOS
                # Use system default output device
                device_id = self._get_default_device()
            else:  # Linux/Raspberry Pi
                # Use device 0 (usually the USB audio device)
                device_id = 0
                
            # Verify device exists
            if device_id is not None:
                device_info = cast(Optional[DeviceInfo], sd.query_devices(device_id))
                if device_info is not None:
                    logger.info(f"Using audio device: {device_info.get('name', 'Unknown')}")
                    
                    # Try to use 44.1kHz first (CD quality), fallback to device default
                    default_rate = device_info.get('default_samplerate', self.DEFAULT_RATE)
                    sample_rate = self._get_supported_rate(self.DEFAULT_RATE)
                    logger.info(f"Using sample rate: {sample_rate} Hz")
                    
                    # Configure device with safe defaults
                    # Note: Ignoring type errors here as sounddevice's types are incomplete
                    sd.default.device = (None, device_id)  # type: ignore
                    sd.default.samplerate = sample_rate  # type: ignore
                    sd.default.channels = (None, 1)  # type: ignore
                else:
                    logger.warning(f"Device {device_id} not found")
            else:
                logger.warning("No suitable audio device found")
                
        except sd.PortAudioError as e:
            logger.error(f"Failed to configure audio device: {e}")
            raise
            
    def _get_supported_rate(self, preferred_rate: float) -> int:
        """Get the closest supported sample rate.
        
        Args:
            preferred_rate: Preferred sample rate
            
        Returns:
            Closest supported sample rate
        """
        # Round to nearest integer
        target = int(round(preferred_rate))
        
        # If the preferred rate is supported, use it
        if target in self.SUPPORTED_RATES:
            return target
            
        # Find the closest supported rate
        # Prefer rates that are multiples/factors of the target
        for rate in self.SUPPORTED_RATES:
            if rate % target == 0 or target % rate == 0:
                return rate
                
        # Fallback to closest rate
        return min(self.SUPPORTED_RATES, key=lambda x: abs(x - target))
            
    def _get_default_device(self) -> Optional[int]:
        """Get the system default output device.
        
        Returns:
            Device ID if found, None otherwise
        """
        try:
            # Get default output device
            default_device = sd.default.device[1]  # Output device
            if default_device is not None:
                return cast(int, default_device)
            
            # Fallback: find first output device
            devices = sd.query_devices()
            for i, device in enumerate(devices):
                device_info = cast(DeviceInfo, device)
                if device_info.get('max_output_channels', 0) > 0:
                    return i
                    
            return None
            
        except Exception as e:
            logger.error(f"Failed to get default device: {e}")
            return None
    
    def play_file(self, file_path: str, volume: Optional[float] = None) -> bool:
        """Play an audio file.
        
        Args:
            file_path: Path to the audio file to play
            volume: Optional volume override (1-11)
            
        Returns:
            True if playback successful, False otherwise
        """
        try:
            # Load the audio file
            data, src_rate = sf.read(file_path)
            
            # Ensure audio data is float32 in range [-1, 1]
            if data.dtype != 'float32':
                data = data.astype('float32')
            
            # Get the device's sample rate
            device_rate = int(sd.default.samplerate)  # type: ignore
            
            # Resample if necessary
            if src_rate != device_rate:
                logger.debug(f"Resampling from {src_rate}Hz to {device_rate}Hz")
                samples = len(data)
                new_samples = int(samples * device_rate / src_rate)
                data = signal.resample(data, new_samples)
            
            # Apply volume scaling
            current_volume = volume if volume is not None else self.volume
            current_volume = max(self.MIN_VOLUME, min(self.MAX_VOLUME, current_volume))
            # Convert 1-11 range to 0-1 range for audio scaling
            volume_scale = (current_volume - 1) / (self.MAX_VOLUME - 1)
            data *= volume_scale
            
            # Play the audio
            sd.play(data, device_rate)
            sd.wait()  # Wait until file is done playing
            return True
            
        except Exception as e:
            logger.error(f"Failed to play audio: {str(e)}")
            return False
    
    def stop(self) -> None:
        """Stop current playback."""
        try:
            sd.stop()
            logger.info("Stopped audio playback")
        except Exception as e:
            logger.error(f"Failed to stop playback: {str(e)}")
    
    @property
    def is_playing(self) -> bool:
        """Check if audio is currently playing.
        
        Returns:
            True if audio is playing, False otherwise
        """
        try:
            return sd.get_stream() is not None
        except Exception:
            return False 