"""Audio playback functionality."""

import platform
from typing import Optional, Dict, Any, Union, cast, TypedDict

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
    
    def __init__(self):
        """Initialize the audio player."""
        self.system = platform.system()
        self._configure_device()
        logger.info(f"Initialized audio player on {self.system}")
        
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
                    
                    # Configure device with safe defaults
                    # Note: Ignoring type errors here as sounddevice's types are incomplete
                    sd.default.device = (None, device_id)  # type: ignore
                    sd.default.samplerate = int(device_info.get('default_samplerate', 44100))  # type: ignore
                    sd.default.channels = (None, 1)  # type: ignore
                else:
                    logger.warning(f"Device {device_id} not found")
            else:
                logger.warning("No suitable audio device found")
                
        except sd.PortAudioError as e:
            logger.error(f"Failed to configure audio device: {e}")
            raise
            
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
    
    def play_file(self, file_path: str) -> bool:
        """Play an audio file.
        
        Args:
            file_path: Path to the audio file to play
            
        Returns:
            True if playback successful, False otherwise
        """
        try:
            # Load the audio file
            data, samplerate = sf.read(file_path)
            
            # Ensure audio data is float32 in range [-1, 1]
            if data.dtype != 'float32':
                data = data.astype('float32')
            
            # Play the audio
            sd.play(data, samplerate)
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