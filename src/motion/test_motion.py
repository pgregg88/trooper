"""Test script for motion detection and response."""

import sys
import time
from pathlib import Path
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.motion.handler import MotionHandler, MotionDirection

def test_motion_responses():
    """Test motion detection responses."""
    # Initialize motion handler
    quotes_file = project_root / "config" / "quotes.yaml"
    handler = MotionHandler(quotes_file)
    
    # Test responses for each direction
    for direction in MotionDirection:
        logger.info(f"\nTesting motion from {direction.value}:")
        
        # Handle motion and play response
        handler.handle_motion(direction)
        
        # Wait for audio to finish
        time.sleep(3)
        
        logger.info(f"Completed {direction.value} test\n")
        time.sleep(1)  # Pause between tests

if __name__ == "__main__":
    test_motion_responses() 