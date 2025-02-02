#!/usr/bin/env python3
"""Stormtrooper Voice Assistant main application."""

import os
import sys
import time
import uuid
from pathlib import Path
import click
from loguru import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/trooper.log", rotation="1 day", retention="7 days", level="DEBUG")

# Import project modules
from src.ai.response_generator import ResponseGenerator
from src.ai.polly_client import PollyClient
from src.ai.lex_client import LexClient
from src.audio.player import AudioPlayer
from src.audio.recorder import AudioRecorder
from src.audio.effects import AudioEffects
from src.motion.pir_handler import PIRHandler
from src.movement.servo_controller import ServoController
from config.settings import Settings
from config.audio_effects import AudioEffectsConfig

class TrooperAssistant:
    """Main Stormtrooper Voice Assistant class."""
    
    def __init__(self):
        """Initialize the assistant."""
        # Load settings
        self.settings = Settings()
        
        # Initialize components
        self.response_gen = ResponseGenerator()
        self.polly = PollyClient()
        self.lex = LexClient(
            bot_id=os.getenv('LEX_BOT_ID', ''),
            bot_alias_id=os.getenv('LEX_BOT_ALIAS_ID', '')
        )
        self.player = AudioPlayer()
        self.recorder = AudioRecorder()
        self.effects = AudioEffects()
        self.pir = PIRHandler(callback=self.handle_motion)
        self.servo = ServoController()
        
        logger.info("Initialized Trooper Assistant")
    
    def handle_motion(self):
        """Handle motion detection event."""
        # Generate response
        response = self.response_gen.get_random_response()
        logger.info(f"Motion detected - Response: {response}")
        
        # Generate speech
        audio_path = self.polly.generate_speech(
            response,
            str(self.settings.audio_cache_dir / f"{uuid.uuid4()}.mp3")
        )
        
        # Apply effects
        processed_path = self.effects.process_file(audio_path)
        
        # Play audio
        self.player.play_file(processed_path)
    
    def cleanup(self):
        """Clean up resources."""
        self.pir.cleanup()
        self.servo.cleanup()
        logger.info("Cleaned up resources")

@click.group()
def cli():
    """Stormtrooper Voice Assistant CLI."""
    pass

@cli.command()
def start():
    """Start the voice assistant."""
    try:
        assistant = TrooperAssistant()
        assistant.pir.start()
        logger.info("Started Trooper Assistant")
        
        # Keep running until interrupted
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping assistant...")
        finally:
            assistant.cleanup()
            
    except Exception as e:
        logger.error(f"Failed to start assistant: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('text')
def speak(text: str):
    """Generate and play a response."""
    try:
        assistant = TrooperAssistant()
        
        # Generate speech
        audio_path = assistant.polly.generate_speech(
            text,
            str(assistant.settings.audio_cache_dir / f"{uuid.uuid4()}.mp3")
        )
        
        # Apply effects
        processed_path = assistant.effects.process_file(audio_path)
        
        # Play audio
        assistant.player.play_file(processed_path)
        
    except Exception as e:
        logger.error(f"Failed to generate speech: {str(e)}")
        sys.exit(1)

@cli.command()
def center():
    """Center the head position."""
    try:
        assistant = TrooperAssistant()
        assistant.servo.center()
        logger.info("Centered head position")
        
    except Exception as e:
        logger.error(f"Failed to center head: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    cli() 