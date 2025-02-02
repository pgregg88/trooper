"""Servo motor controller for head movement."""

import time
from typing import Optional, Tuple
from loguru import logger

try:
    import RPi.GPIO as GPIO
except ImportError:
    logger.warning("RPi.GPIO not available - running in mock mode")
    GPIO = None

class ServoController:
    """Servo motor controller for head movement."""
    
    def __init__(self, 
                 pan_pin: int = 18, 
                 tilt_pin: int = 27,
                 freq: int = 50):
        """Initialize servo controller.
        
        Args:
            pan_pin: GPIO pin for pan servo
            tilt_pin: GPIO pin for tilt servo
            freq: PWM frequency in Hz
        """
        self.pan_pin = pan_pin
        self.tilt_pin = tilt_pin
        self.freq = freq
        
        # Current angles
        self.current_pan = 90
        self.current_tilt = 90
        
        if GPIO:
            GPIO.setmode(GPIO.BCM)
            
            # Setup pan servo
            GPIO.setup(self.pan_pin, GPIO.OUT)
            self.pan_pwm = GPIO.PWM(self.pan_pin, freq)
            self.pan_pwm.start(self._angle_to_duty_cycle(90))
            
            # Setup tilt servo
            GPIO.setup(self.tilt_pin, GPIO.OUT)
            self.tilt_pwm = GPIO.PWM(self.tilt_pin, freq)
            self.tilt_pwm.start(self._angle_to_duty_cycle(90))
            
            logger.info(f"Initialized servos on pins: pan={pan_pin}, tilt={tilt_pin}")
        else:
            logger.warning("Running in mock mode - servo control disabled")
            self.pan_pwm = None
            self.tilt_pwm = None
    
    def _angle_to_duty_cycle(self, angle: float) -> float:
        """Convert angle to duty cycle.
        
        Args:
            angle: Angle in degrees (0-180)
            
        Returns:
            Duty cycle (2-12)
        """
        return ((angle / 18) + 2)
    
    def set_position(self, pan: Optional[float] = None, tilt: Optional[float] = None):
        """Set servo positions.
        
        Args:
            pan: Pan angle in degrees (0-180)
            tilt: Tilt angle in degrees (0-180)
        """
        if pan is not None:
            pan = max(0, min(180, pan))
            if GPIO and self.pan_pwm:
                self.pan_pwm.ChangeDutyCycle(self._angle_to_duty_cycle(pan))
            self.current_pan = pan
            logger.debug(f"Set pan to {pan}°")
            
        if tilt is not None:
            tilt = max(0, min(180, tilt))
            if GPIO and self.tilt_pwm:
                self.tilt_pwm.ChangeDutyCycle(self._angle_to_duty_cycle(tilt))
            self.current_tilt = tilt
            logger.debug(f"Set tilt to {tilt}°")
    
    def get_position(self) -> Tuple[float, float]:
        """Get current servo positions.
        
        Returns:
            Tuple of (pan, tilt) angles in degrees
        """
        return (self.current_pan, self.current_tilt)
    
    def center(self):
        """Center both servos to 90 degrees."""
        self.set_position(90, 90)
        logger.info("Centered servos")
    
    def cleanup(self):
        """Clean up GPIO resources."""
        if GPIO:
            if self.pan_pwm:
                self.pan_pwm.stop()
            if self.tilt_pwm:
                self.tilt_pwm.stop()
            GPIO.cleanup()
        logger.info("Cleaned up servo controller") 