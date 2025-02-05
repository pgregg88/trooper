#!/usr/bin/env python3
"""Stormtrooper Voice Assistant CLI.

This script provides a command-line interface to the Stormtrooper voice system.
"""

import sys
import shlex
import argparse
from pathlib import Path
from typing import Optional, List
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.audio.processor import process_and_play_text
from src.audio import AudioError

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI.
    
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="Stormtrooper Voice Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (use single quotes around text):
  trooper say 'Stop right there!'
  
  # With volume (1-11):
  trooper say -v 11 'Intruder alert!'
  
  # Full options:
  trooper say --volume 11 --urgency high --context combat 'Enemy spotted!'
  
  # Generate without playing:
  trooper say --no-play --keep 'All clear'
  
Note: If your text contains special characters, wrap it in single quotes (')
      For Windows users, use double quotes (") instead.
"""
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # 'say' command
    say_parser = subparsers.add_parser(
        "say",
        help="Convert text to Stormtrooper speech",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    say_parser.add_argument(
        "text",
        help="Text to convert to speech (wrap in quotes if it contains spaces)"
    )
    
    say_parser.add_argument(
        "-v", "--volume",
        type=float,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        help="Volume level (1-11, default: 5)"
    )
    
    say_parser.add_argument(
        "-u", "--urgency",
        choices=["low", "normal", "high"],
        default="normal",
        help="Voice urgency level (default: normal)"
    )
    
    say_parser.add_argument(
        "-c", "--context",
        choices=["general", "combat", "alert", "patrol"],
        default="general",
        help="Voice context (default: general)"
    )
    
    say_parser.add_argument(
        "--no-play",
        action="store_true",
        help="Generate audio without playing"
    )
    
    say_parser.add_argument(
        "--keep",
        action="store_true",
        help="Keep generated audio files"
    )
    
    return parser

def handle_say(args: argparse.Namespace) -> int:
    """Handle the 'say' command.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Process text to speech
        output_path = process_and_play_text(
            text=args.text,
            urgency=args.urgency,
            context=args.context,
            play_immediately=not args.no_play,
            cleanup=not args.keep,
            volume=args.volume
        )
        
        # Print output path if keeping file
        if args.keep:
            print(f"\nAudio file saved to: {output_path}")
            
        return 0
        
    except AudioError as e:
        logger.error(f"Audio processing failed: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 2

def main() -> int:
    """Run the CLI application.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    
    try:
        args = parser.parse_args()
    except Exception as e:
        logger.error("Error parsing arguments. Make sure to wrap text in quotes!")
        logger.error("Example: trooper say 'Stop right there!'")
        return 1
    
    if not args.command:
        parser.print_help()
        return 0
        
    if args.command == "say":
        return handle_say(args)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 