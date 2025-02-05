"""Script to test different Polly voices for Stormtrooper voice."""

import os
from pathlib import Path
from typing import List, Dict, Optional
import boto3
import yaml
from loguru import logger

class VoiceTester:
    """Test different Polly voices for Stormtrooper voice."""
    
    def __init__(self, profile_name: str = 'trooper', region_name: str = 'us-east-1'):
        """Initialize Polly client with AWS credentials.
        
        Args:
            profile_name: AWS profile name
            region_name: AWS region name
        """
        self.polly = boto3.Session(
            profile_name=profile_name,
            region_name=region_name
        ).client('polly')
        
        # Create output directory
        self.output_dir = Path('assets/audio/polly_raw')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load quotes
        self.quotes = self._load_quotes()
        
    def _load_quotes(self) -> Dict:
        """Load quotes from YAML file.
        
        Returns:
            Dictionary of quote categories and their quotes
        """
        quotes_path = Path('docs/stormtrooper_quotes.yaml')
        with open(quotes_path, 'r') as f:
            return yaml.safe_load(f)
        
    def generate_test_audio(self, voice_configs: List[Dict]) -> None:
        """Generate test audio for each voice configuration.
        
        Args:
            voice_configs: List of voice configuration dictionaries containing:
                         - voice_id: Polly voice ID
                         - category: Quote category to use
                         - quote_index: Index of quote to use from category
                         - description: Description of this variation
        """
        for config in voice_configs:
            try:
                voice_id = config['voice_id']
                category = config['category']
                quote_index = config['quote_index']
                description = config.get('description', '')
                
                # Get quote from specified category and index
                text = self.quotes[category][quote_index]
                
                # Request PCM format from Polly (16kHz is supported)
                response = self.polly.synthesize_speech(
                    Text=text,
                    TextType='text',
                    OutputFormat='pcm',
                    SampleRate='16000',  # 16kHz is supported by Polly
                    VoiceId=voice_id,
                    Engine='neural'
                )
                
                if "AudioStream" not in response:
                    logger.error(f"No AudioStream in response for voice {voice_id}")
                    continue
                
                # Create filename with category and description
                output_file = self.output_dir / f"{voice_id}_neural_{category}_{description.lower().replace(' ', '_')}.wav"
                
                # Convert PCM to WAV using soundfile
                import soundfile as sf
                import numpy as np
                from scipy import signal
                
                # Read PCM data as int16
                audio_data = np.frombuffer(response['AudioStream'].read(), dtype=np.int16)
                # Convert to float32 normalized between -1 and 1
                audio_data = audio_data.astype(np.float32) / 32768.0
                
                # Resample to 44.1kHz for better quality
                audio_data = signal.resample(audio_data, int(len(audio_data) * 44100 / 16000))
                
                # Save as WAV
                sf.write(str(output_file), audio_data, 44100, format='WAV', subtype='PCM_16')
                    
                logger.info(f"Generated test audio: {output_file}")
                logger.info(f"Category: {category}")
                logger.info(f"Description: {description}")
                logger.info(f"Text used: {text}")
                
            except Exception as e:
                logger.error(f"Failed to generate audio for config {config}: {str(e)}")

def main():
    """Main function to run voice tests."""
    # Test configurations using different quote categories
    voice_configs = [
        # Spotted quotes
        {
            'voice_id': 'Matthew',
            'category': 'spotted',
            'quote_index': 0,  # "Adversary inbound"
            'description': 'Alert'
        },
        {
            'voice_id': 'Matthew',
            'category': 'spotted',
            'quote_index': 2,  # "Jedi!"
            'description': 'Urgent'
        },
        
        # Taunt quotes
        {
            'voice_id': 'Matthew',
            'category': 'taunt',
            'quote_index': 1,  # "Surrender!"
            'description': 'Command'
        },
        {
            'voice_id': 'Matthew',
            'category': 'taunt',
            'quote_index': 5,  # "You're under arrest!"
            'description': 'Authority'
        },
        
        # Squad commands
        {
            'voice_id': 'Matthew',
            'category': 'squad_commands',
            'quote_index': 12,  # "Steady! Concentrate fire!"
            'description': 'Tactical'
        },
        
        # Conversation
        {
            'voice_id': 'Matthew',
            'category': 'conversation',
            'quote_index': 8,  # "Present your identity card for verification."
            'description': 'Official'
        }
    ]
    
    # Create tester and generate samples
    tester = VoiceTester()
    tester.generate_test_audio(voice_configs)
    
if __name__ == '__main__':
    main() 