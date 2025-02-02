"""AWS Polly integration for text-to-speech."""

import os
from pathlib import Path
import boto3
from loguru import logger

class PollyClient:
    """AWS Polly client for text-to-speech synthesis."""
    
    def __init__(self, profile_name='trooper', region_name='us-east-1'):
        """Initialize Polly client with AWS credentials."""
        try:
            self.polly = boto3.Session(
                profile_name=profile_name,
                region_name=region_name
            ).client('polly')
            self.voice_id = "Matthew"  # Default voice
            logger.info(f"Initialized Polly client with voice: {self.voice_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Polly client: {str(e)}")
            raise
    
    def generate_speech(self, text: str, output_path: str = None) -> bytes:
        """Generate speech from text using Polly.
        
        Args:
            text: The text to convert to speech
            output_path: Optional path to save the audio file
            
        Returns:
            Raw audio data if no output_path is provided,
            otherwise returns the path to the saved file
        """
        try:
            response = self.polly.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=self.voice_id,
                Engine='neural'
            )
            
            if "AudioStream" not in response:
                raise ValueError("No AudioStream in Polly response")
            
            audio_data = response['AudioStream'].read()
            
            if output_path:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'wb') as f:
                    f.write(audio_data)
                logger.info(f"Saved audio to: {output_path}")
                return str(output_path)
            
            return audio_data
            
        except Exception as e:
            logger.error(f"Failed to generate speech: {str(e)}")
            raise
    
    def set_voice(self, voice_id: str) -> None:
        """Change the Polly voice ID."""
        self.voice_id = voice_id
        logger.info(f"Changed voice to: {voice_id}") 