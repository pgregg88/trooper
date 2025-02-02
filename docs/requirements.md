# **Technical Requirements Document**  
## **Project: Life-Size Stormtrooper AI Voice Assistant**  
📅 **Version:** 1.1  
📍 **Last Updated:** [Current Date]  

---

## **1️⃣ Overview**  
This document outlines the technical setup for a life-size Stormtrooper head with motion detection, servo-controlled movement, and voice response capabilities. The system uses a combination of pre-recorded audio and AI-generated speech for responses.

---

## **2️⃣ System Requirements**  

### **2.1 Hardware**
- **Raspberry Pi 4 Model B**
- **64GB SD Card** with Raspberry Pi OS Minimal (64-bit)
- **USB Microphone**
- **Self-powered USB Speaker**
- **Adafruit PCA9685 Servo Controller**
- **3 Servos** for head movement (pan, tilt, roll)
- **2 PIR Motion Sensors** (installed in eye locations)
- **Power Supplies:**
  - Dedicated supply for Raspberry Pi
  - Dedicated supply for servos

### **2.2 Development Environment**
- **IDE:** Cursor (VSCode-based)
- **Development Machine:** Mac with SSH access to RPi
- **Project Location:** `/home/pgregg/trooper`
- **Python Version:** 3.11.2 (venv)
- **Git:** Configured with remote origin
- **AWS:** Local credentials configured with --profile trooper

### **2.3 Raspberry Pi Configuration**
- Fresh installation of Pi OS minimal 64-bit
- Enabled via raspi-config:
  - WiFi
  - Expanded filesystem
  - I2C
  - SSH
- Python virtual environment
- Git installed and configured

---

## **3️⃣ Software Dependencies**
See `requirements.txt` for specific version requirements.

### **3.1 Core Components**
- Git integration
- Environment management
- Logging system

### **3.2 AWS & AI Services**
- Amazon Polly for voice synthesis
- Amazon Lex for conversation (planned)
- AWS SDK (boto3)

### **3.3 Audio Processing**
- Real-time audio capture and playback
- Speech recognition
- Voice effect processing
- Audio file management

### **3.4 Hardware Control**
- Servo control via I2C
- PIR sensor input
- GPIO management

---

## **4️⃣ Project Structure**
```
/home/pgregg/trooper/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── audio_effects.py
├── src/
│   ├── motion/
│   │   ├── __init__.py
│   │   └── pir_handler.py
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── player.py
│   │   ├── recorder.py
│   │   └── effects.py
│   ├── movement/
│   │   ├── __init__.py
│   │   └── servo_controller.py
│   └── ai/
│       ├── __init__.py
│       ├── polly_client.py
│       └── lex_client.py
├── assets/
│   └── audio/
│       ├── cache/
│       └── responses/
├── tests/
└── main.py
```

---

## **5️⃣ System Behavior**

### **5.1 Motion Detection**
- Dual PIR sensors for direction detection
- Debounce implementation to prevent false triggers
- Movement triggers audio and servo response

### **5.2 Audio Response**
- Local pre-recorded audio for immediate response
- AI-generated speech for dynamic responses
- Audio effect processing for authentic Stormtrooper voice
- Caching system for generated responses

### **5.3 Head Movement**
- Synchronized with audio responses
- Multiple movement patterns
- Position limits for safe operation

---

## **6️⃣ Testing & Deployment**

### **6.1 Testing**
Focus on critical path testing:
- Audio playback verification
- Motion sensor reliability
- Servo movement limits
- Basic integration tests

### **6.2 Deployment**
1. Clone repository to RPi
2. Set up virtual environment
3. Install dependencies
4. Configure AWS credentials
5. Run system tests
6. Start main application

---

## **7️⃣ Future Enhancements**
- Integration with Amazon Lex for conversation
- Enhanced motion tracking
- Additional movement patterns
- Extended voice command recognition

---

## **🔧 Troubleshooting**
| **Issue** | **Solution** |
|-----------|-------------|
| **No audio output** | Run `alsamixer` and set the correct output device. |
| **Microphone not detected** | Run `arecord -l` and check `asound.conf`. |
| **Polly not working** | Ensure AWS credentials are set up correctly. |
| **Servos not moving** | Check I2C is enabled (`sudo raspi-config`). |

---

## **🎯 Final Notes**
- **By following this guide, developers can quickly set up the environment and begin working on the Stormtrooper AI voice assistant.**  
- **Ensure API keys are kept private and not shared in repositories.**  
- **Future enhancements include adding a wake word, cloud-based logging, and Wi-Fi remote control.**  

---

Would you like to include **multi-language support** or **additional sound effects for realism**? 🚀🎙️