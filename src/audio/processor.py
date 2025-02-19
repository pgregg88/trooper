"""Text-to-speech processor with Stormtrooper voice effect and playback.

This module combines TTS generation, audio processing, and playback into a single pipeline.
"""

import sys
from pathlib import Path
from typing import Optional
import numpy as np
import soundfile as sf
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.audio.polly import PollyClient
from src.audio.effects import StormtrooperEffect
from src.audio import AudioPlayer, AudioError

def process_and_play_text(
    text: str,
    urgency: str = "normal",
    context: str = "general",
    play_immediately: bool = True,
    cleanup: bool = True,
    volume: Optional[float] = None
) -> Path:
    """Process text through TTS pipeline and optionally play it.
    
    Args:
        text: Input text to process
        urgency: Urgency level (default: "normal")
        context: Context for voice generation (default: "general")
        play_immediately: Whether to play the audio after processing
        cleanup: Whether to delete the temporary files after processing
        volume: Optional volume level from 1 (quietest) to 11 (loudest)
        
    Returns:
        Path to the processed audio file
        
    Raises:
        AudioError: If there's an error during processing or playback
    """
    try:
        # Setup directories
        temp_dir = project_root / "assets" / "audio" / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Clean text for filename
        clean_text = "_".join(text.split()[:3]).lower()
        clean_text = "".join(c for c in clean_text if c.isalnum() or c == "_")
        
        # Generate filenames
        base_name = f"temp_{clean_text}"
        raw_path = temp_dir / f"{base_name}_raw.wav"
        processed_path = temp_dir / f"{base_name}_processed.wav"
        
        # Initialize components
        polly = PollyClient()
        effect = StormtrooperEffect()
        
        # Generate raw audio
        logger.info(f"Generating TTS for: {text}")
        pcm_data = polly.generate_speech(
            text=text,
            urgency=urgency,
            context=context
        )
        
        if not isinstance(pcm_data, bytes):
            raise AudioError("Expected bytes from Polly TTS")
            
        # Convert PCM bytes to float32 array
        audio_data = np.frombuffer(pcm_data, dtype=np.int16)
        audio_float = audio_data.astype(np.float32) / 32768.0
        
        # Save raw audio
        sf.write(str(raw_path), audio_float, 16000, format='WAV', subtype='FLOAT')
        
        # Apply effects
        logger.info("Applying Stormtrooper effect...")
        effect.process_file(
            str(raw_path),
            str(processed_path)
        )
        
        # Play if requested
        if play_immediately:
            logger.info("Playing processed audio...")
            player = AudioPlayer()
            if volume is not None:
                player.set_volume(volume)
            player.play_file(str(processed_path))
        
        # Cleanup if requested
        if cleanup:
            raw_path.unlink(missing_ok=True)
            
        return processed_path
            
    except Exception as e:
        raise AudioError(f"Error processing audio: {str(e)}") 