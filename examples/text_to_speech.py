#!/usr/bin/env python3
"""Example script demonstrating text-to-speech with Stormtrooper effect."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.audio.processor import process_and_play_text

def main():
    """Run text-to-speech example."""
    # Example 1: Basic usage (default volume)
    text = "Stop right there! You're under arrest!"
    process_and_play_text(text)
    
    # Example 2: With different urgency and context (loud volume)
    text = "Alert! Intruder detected in sector 7!"
    process_and_play_text(
        text,
        urgency="high",
        context="alert",
        volume=11  # Maximum volume
    )
    
    # Example 3: Generate without playing
    text = "All clear. Resuming normal patrol."
    output_path = process_and_play_text(
        text,
        play_immediately=False,
        cleanup=False  # Keep the file
    )
    print(f"\nGenerated audio file saved to: {output_path}")
    
    # Example 4: Different volume levels
    text = "Testing volume levels..."
    for volume in [1, 5, 11]:
        print(f"\nPlaying at volume level {volume}")
        process_and_play_text(text, volume=volume)

if __name__ == "__main__":
    main() 