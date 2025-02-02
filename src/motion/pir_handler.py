"""PIR motion sensor handler."""

import time
from typing import Callable, Optional
from loguru import logger

try:
    import RPi.GPIO as GPIO
except ImportError:
    logger.warning("RPi.GPIO not available - running in mock mode")
    GPIO = None

class PIRHandler:
    """PIR motion sensor handler."""
    
    def __init__(self, pin: int = 17, callback: Optional[Callable] = None):
        """Initialize PIR handler.
        
        Args:
            pin: GPIO pin number for PIR sensor
            callback: Optional callback function when motion detected
        """
        self.pin = pin
        self.callback = callback
        self.is_active = False
        
        if GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN)
            logger.info(f"Initialized PIR sensor on pin {pin}")
        else:
            logger.warning("Running in mock mode - PIR sensor disabled")
    
    def start(self):
        """Start motion detection."""
        self.is_active = True
        if GPIO:
            GPIO.add_event_detect(
                self.pin, 
                GPIO.RISING,
                callback=self._motion_detected
            )
        logger.info("Started motion detection")
    
    def stop(self):
        """Stop motion detection."""
        self.is_active = False
        if GPIO:
            GPIO.remove_event_detect(self.pin)
        logger.info("Stopped motion detection")
    
    def _motion_detected(self, channel):
        """Handle motion detection event."""
        if self.callback:
            self.callback()
        logger.info("Motion detected!")
    
    def cleanup(self):
        """Clean up GPIO resources."""
        if GPIO:
            GPIO.cleanup()
        logger.info("Cleaned up PIR handler") 