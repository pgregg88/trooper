"""Real-time text-to-speech with Stormtrooper effects."""

import asyncio
from typing import Optional
import threading
from queue import Queue
import tempfile
from pathlib import Path
import os
import subprocess
from loguru import logger

from src.audio.effects import StormtrooperEffect
from src.audio.polly import PollyClient
from src.quotes import UrgencyLevel

class RealtimeStormtrooperTTS:
    """Real-time text-to-speech with Stormtrooper effects."""
    
    def __init__(self):
        """Initialize the real-time TTS system."""
        self.effect = StormtrooperEffect()
        self.polly = PollyClient()
        self.audio_queue: Queue = Queue()
        self.current_task: Optional[asyncio.Task] = None
        self.current_process: Optional[subprocess.Popen] = None
        self.is_speaking = False
        self.temp_dir = Path(tempfile.mkdtemp(prefix="trooper_tts_"))
        
        # Start audio processing thread
        self.processing_thread = threading.Thread(target=self._process_audio_queue)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        logger.info("Initialized real-time Stormtrooper TTS")
        
    async def speak(self, text: str, urgency: UrgencyLevel = UrgencyLevel.MEDIUM, context: str = 'patrol'):
        """Speak text with Stormtrooper effects.
        
        Args:
            text: Text to speak
            urgency: Urgency level for effects
            context: Context for SSML template
        """
        # Cancel current speech if any
        if self.current_task is not None:
            self.current_task.cancel()
            try:
                await self.current_task
            except asyncio.CancelledError:
                pass
            
        # Stop current audio if playing
        if self.current_process is not None:
            self.current_process.terminate()
            self.current_process = None
        
        # Create new speech task
        self.current_task = asyncio.create_task(self._generate_and_play(text, urgency, context))
        await self.current_task
        
    async def _generate_and_play(self, text: str, urgency: UrgencyLevel, context: str):
        """Generate and play audio for text.
        
        Args:
            text: Text to speak
            urgency: Urgency level for effects
            context: Context for SSML template
        """
        try:
            # Create temp files
            temp_pcm = self.temp_dir / f"{hash(text)}.pcm"
            temp_wav = self.temp_dir / f"{hash(text)}.wav"
            
            # Generate speech using existing pipeline
            self.polly.generate_speech(
                text,
                output_path=str(temp_pcm),
                urgency=urgency.value,
                context=context
            )
            
            # Set effect urgency
            self.effect.set_urgency(urgency)
            
            # Process with effects (this handles sample rate conversion)
            self.effect.process_file(
                str(temp_pcm),
                str(temp_wav)
            )
            
            # Clean up PCM file
            temp_pcm.unlink()
            
            # Queue WAV for playback
            self.audio_queue.put(temp_wav)
            logger.debug(f"Queued audio for text: {text[:30]}...")
            
        except Exception as e:
            logger.error(f"Error generating speech: {str(e)}")
            
    def _process_audio_queue(self):
        """Process and play queued audio."""
        while True:
            try:
                # Get next audio file
                audio_file = self.audio_queue.get()
                
                # Play audio using system player
                self.is_speaking = True
                self.current_process = subprocess.Popen(['afplay', str(audio_file)])
                self.current_process.wait()
                self.current_process = None
                self.is_speaking = False
                
                # Clean up temp file
                audio_file.unlink()
                
            except Exception as e:
                logger.error(f"Error processing audio queue: {str(e)}")
                
    def close(self):
        """Clean up resources."""
        if self.current_task is not None:
            self.current_task.cancel()
            
        if self.current_process is not None:
            self.current_process.terminate()
            
        # Clean up temp directory
        for file in self.temp_dir.glob("*.*"):
            try:
                file.unlink()
            except:
                pass
        try:
            self.temp_dir.rmdir()
        except:
            pass
            
        logger.info("Closed real-time TTS system") 