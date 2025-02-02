"""Audio recording functionality."""

import threading
from pathlib import Path
from typing import Optional, Callable
import sounddevice as sd
import soundfile as sf
import numpy as np
from loguru import logger

class AudioRecorder:
    """Audio recorder for capturing voice input."""
    
    def __init__(self, 
                 samplerate: int = 44100,
                 channels: int = 1,
                 dtype: str = 'float32'):
        """Initialize audio recorder.
        
        Args:
            samplerate: Sample rate in Hz
            channels: Number of audio channels
            dtype: Data type for audio samples
        """
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.recording = False
        self.audio_data = []
        self._record_thread = None
        
        logger.info(f"Initialized audio recorder: {samplerate}Hz, {channels} channels")
    
    def start_recording(self, callback: Optional[Callable] = None):
        """Start recording audio.
        
        Args:
            callback: Optional callback function when recording is complete
        """
        if self.recording:
            logger.warning("Already recording")
            return
        
        self.recording = True
        self.audio_data = []
        
        def record_audio():
            """Record audio in a separate thread."""
            with sd.InputStream(samplerate=self.samplerate,
                              channels=self.channels,
                              dtype=self.dtype) as stream:
                
                while self.recording:
                    data, overflowed = stream.read(1024)
                    if overflowed:
                        logger.warning("Audio input overflow")
                    self.audio_data.append(data.copy())
                
                if callback:
                    callback()
        
        self._record_thread = threading.Thread(target=record_audio)
        self._record_thread.start()
        logger.info("Started recording")
    
    def stop_recording(self) -> np.ndarray:
        """Stop recording and return the recorded audio data.
        
        Returns:
            Numpy array of recorded audio data
        """
        if not self.recording:
            logger.warning("Not currently recording")
            return np.array([])
        
        self.recording = False
        if self._record_thread:
            self._record_thread.join()
        
        # Combine all audio chunks
        audio_data = np.concatenate(self.audio_data, axis=0)
        logger.info(f"Stopped recording: {len(audio_data)} samples")
        
        return audio_data
    
    def save_recording(self, filepath: str, data: Optional[np.ndarray] = None):
        """Save recorded audio to file.
        
        Args:
            filepath: Path to save audio file
            data: Optional audio data to save. If None, uses last recording
        """
        try:
            # Use provided data or last recording
            save_data = data if data is not None else np.concatenate(self.audio_data, axis=0)
            
            # Create directory if needed
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # Save audio file
            sf.write(filepath, save_data, self.samplerate)
            logger.info(f"Saved recording to: {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save recording: {str(e)}")
            raise
    
    @property
    def is_recording(self) -> bool:
        """Check if currently recording."""
        return self.recording 