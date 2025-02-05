"""Example demonstrating real-time Stormtrooper TTS usage."""

import asyncio
import time
from loguru import logger

from src.audio.realtime import RealtimeStormtrooperTTS
from src.quotes import UrgencyLevel

async def demo_basic_speech(tts: RealtimeStormtrooperTTS):
    """Demonstrate basic speech synthesis."""
    logger.info("Basic speech demo...")
    await tts.speak("Sector clear", context='patrol')
    await asyncio.sleep(2)  # Wait for speech to finish

async def demo_urgency_levels(tts: RealtimeStormtrooperTTS):
    """Demonstrate different urgency levels."""
    logger.info("Urgency levels demo...")
    
    # High urgency combat
    await tts.speak("Stop right there!", UrgencyLevel.HIGH, context='combat')
    await asyncio.sleep(2)
    
    # Medium urgency patrol
    await tts.speak("Checking the perimeter", UrgencyLevel.MEDIUM, context='patrol')
    await asyncio.sleep(2)
    
    # Low urgency inspection
    await tts.speak("All clear", UrgencyLevel.LOW, context='inspection')
    await asyncio.sleep(2)

async def demo_interruption(tts: RealtimeStormtrooperTTS):
    """Demonstrate speech interruption."""
    logger.info("Speech interruption demo...")
    
    # Start a long patrol message
    logger.info("Starting patrol report...")
    task = asyncio.create_task(
        tts.speak(
            "This is a routine patrol report. Nothing unusual to report. "
            "Continuing standard sweep of the area. Maintaining regular patrol pattern.",
            context='patrol'
        )
    )
    
    # Wait a bit then interrupt with alert
    await asyncio.sleep(2)
    logger.info("Interrupting with alert...")
    await tts.speak("Alert! Intruder detected!", UrgencyLevel.HIGH, context='alert')
    
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Previous speech was interrupted as expected")

async def main():
    """Run the TTS demonstration."""
    logger.info("Starting TTS demo")
    
    # Create TTS instance
    tts = RealtimeStormtrooperTTS()
    
    try:
        # Basic speech
        await demo_basic_speech(tts)
        
        # Different urgency levels
        await demo_urgency_levels(tts)
        
        # Speech interruption
        await demo_interruption(tts)
        
        logger.info("Demo completed successfully")
        
    except Exception as e:
        logger.error(f"Demo failed: {str(e)}")
        raise
        
    finally:
        # Clean up
        tts.close()
        logger.info("Cleaned up TTS resources")

if __name__ == "__main__":
    # Configure logging
    logger.add("tts_demo.log", rotation="1 MB")
    
    # Run the demo
    asyncio.run(main()) 