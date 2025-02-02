# Stormtrooper Voice Assistant

A Raspberry Pi-powered Stormtrooper voice assistant that responds to motion with authentic Imperial responses.

## Features

- Motion detection using PIR sensors
- Pan/tilt head movement with servo motors
- Text-to-speech using AWS Polly
- Stormtrooper voice effects processing
- Configurable responses and behaviors

## Requirements

- Raspberry Pi (3 or newer recommended)
- PIR motion sensor
- 2x servo motors (pan/tilt)
- Speaker/audio output
- Python 3.8+
- AWS account with Polly access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/trooper.git
cd trooper
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure AWS credentials:
```bash
aws configure --profile trooper
```

## Project Structure

```
trooper/
├── src/
│   ├── ai/
│   │   ├── polly_client.py      # AWS Polly integration
│   │   └── response_generator.py # Response generation
│   ├── audio/
│   │   ├── effects.py           # Audio effects processing
│   │   └── player.py            # Audio playback
│   ├── motion/
│   │   └── pir_handler.py       # Motion detection
│   └── movement/
│       └── servo_controller.py   # Servo control
├── config/
│   ├── settings.py              # Global settings
│   └── audio_effects.py         # Audio effects config
├── assets/
│   └── audio/                   # Audio file storage
├── requirements.txt
└── README.md
```

## Usage

1. Start the voice assistant:
```bash
python main.py
```

2. Available commands:
```bash
# Start motion detection
python main.py start

# Test voice response
python main.py speak "Move along, citizen."

# Center head position
python main.py center

# Stop all services
python main.py stop
```

## Configuration

- Edit `config/settings.py` to modify global settings
- Edit `config/audio_effects.py` to adjust voice effects
- Add custom responses in `src/ai/response_generator.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.