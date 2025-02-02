"""Motion detection simulator for testing."""

import sys
import time
import random
from pathlib import Path
from typing import Optional, Callable, List
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.motion.types import MotionDirection
from src.motion.handler import MotionHandler

class MotionSimulator:
    """Simulates motion detection events."""
    
    def __init__(
        self,
        handler: Optional[MotionHandler] = None,
        quotes_file: Optional[Path] = None,
        config_file: Optional[Path] = None
    ):
        """Initialize the motion simulator.
        
        Args:
            handler: Optional motion handler to use
            quotes_file: Optional path to quotes file
            config_file: Optional path to motion response config
        """
        if handler is None:
            quotes_file = quotes_file or (project_root / "config" / "quotes.yaml")
            config_file = config_file or (project_root / "config" / "motion_responses.yaml")
            handler = MotionHandler(quotes_file, config_file)
            
        self.handler = handler
        
    def simulate_random_motion(self, duration: int = 30, interval: float = 3.0) -> None:
        """Simulate random motion events.
        
        Args:
            duration: How long to run simulation in seconds
            interval: Minimum interval between events in seconds
        """
        logger.info(f"Starting motion simulation for {duration} seconds")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Random direction
            direction = random.choice(list(MotionDirection))
            logger.info(f"Simulating motion from {direction.value}")
            
            # Handle motion
            self.handler.handle_motion(direction)
            
            # Wait random interval
            wait_time = interval + random.uniform(0, 2.0)
            time.sleep(wait_time)
            
        logger.info("Motion simulation complete")
        
    def simulate_sequence(self, sequence: list[MotionDirection], interval: float = 3.0) -> None:
        """Simulate a specific sequence of motion events.
        
        Args:
            sequence: List of motion directions to simulate
            interval: Time between events in seconds
        """
        logger.info(f"Starting motion sequence simulation with {len(sequence)} events")
        
        for direction in sequence:
            logger.info(f"Simulating motion from {direction.value}")
            self.handler.handle_motion(direction)
            time.sleep(interval)
            
        logger.info("Motion sequence complete")

def main():
    """Run motion simulation."""
    simulator = MotionSimulator()
    
    # Test random motion
    simulator.simulate_random_motion(duration=20)
    
    # Test specific sequence
    sequence = [
        MotionDirection.LEFT,
        MotionDirection.CENTER,
        MotionDirection.RIGHT,
        MotionDirection.UNKNOWN
    ]
    simulator.simulate_sequence(sequence)

if __name__ == "__main__":
    main() 