# Trooper Voice Assistant

A command-line tool that converts text to speech with a Stormtrooper voice effect.

## Features

- Text-to-speech using Amazon Polly
- Stormtrooper voice effect processing
- Volume control (1-11)
- Multiple voice contexts (general, combat, alert, patrol)
- Urgency levels (low, normal, high)
- Audio file management
- Command-line interface

## Installation

### Prerequisites

1. Python 3.8 or higher
2. pip (Python package installer)
3. Virtual environment tool (venv)
4. AWS account with Polly access

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd trooper
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate it
   # On macOS/Linux:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install the Package**
   ```bash
   # Install in development mode
   pip install -e .
   ```

4. **Configure AWS Credentials**
   
   The tool requires AWS credentials for Amazon Polly. You can configure these in several ways:

   a. Using AWS CLI:
   ```bash
   aws configure
   ```

   b. Environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID="your_access_key"
   export AWS_SECRET_ACCESS_KEY="your_secret_key"
   export AWS_DEFAULT_REGION="us-east-1"
   ```

   c. Credentials file:
   ```ini
   # ~/.aws/credentials
   [default]
   aws_access_key_id = your_access_key
   aws_secret_access_key = your_secret_key
   ```

5. **Verify Installation**
   ```bash
   # Check if trooper command is available
   which trooper  # Should point to .venv/bin/trooper

   # Check help
   trooper --help
   ```

## Usage

### Basic Commands

1. **Basic Text-to-Speech**
   ```bash
   trooper say 'Stop right there!'
   ```

2. **Adjust Volume (1-11)**
   ```bash
   trooper say -v 11 'Intruder alert!'
   ```

3. **Set Urgency and Context**
   ```bash
   trooper say --volume 11 --urgency high --context combat 'Enemy spotted!'
   ```

4. **Generate Without Playing**
   ```bash
   trooper say --no-play --keep 'All clear'
   ```

### Command Options

- `-v, --volume`: Set volume level (1-11, default: 5)
- `-u, --urgency`: Set urgency level (low, normal, high)
- `-c, --context`: Set voice context (general, combat, alert, patrol)
- `--no-play`: Generate audio without playing
- `--keep`: Keep generated audio files

## Troubleshooting

### Common Issues

1. **Command Not Found**
   ```bash
   # Solution: Make sure virtual environment is activated
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows
   ```

2. **Import Errors**
   ```bash
   # Solution: Reinstall the package
   pip uninstall trooper
   pip install -e .
   ```

3. **Audio Device Issues**
   - Check if your system's audio device is working
   - Try adjusting volume
   - Check system audio settings
   ```bash
   # Test audio
   trooper say --volume 5 'Test'
   ```

4. **AWS Credentials Issues**
   - Verify AWS credentials are properly configured
   - Check AWS IAM permissions for Polly
   - Ensure correct region is set
   ```bash
   # Test AWS configuration
   aws polly describe-voices
   ```

### Audio Quality Issues

1. **Volume Too Low**
   ```bash
   # Increase volume (max 11)
   trooper say -v 11 'Test volume'
   ```

2. **Audio Distortion**
   ```bash
   # Try lower volume
   trooper say -v 5 'Test audio'
   ```

3. **Playback Issues**
   ```bash
   # Generate file without playing
   trooper say --no-play --keep 'Test'
   # Then play with system audio player
   ```

## Development

### Running Tests
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Code Style
The project uses:
- Black for code formatting
- Ruff for linting
- MyPy for type checking

### Building from Source
```bash
# Install build dependencies
pip install build

# Build package
python -m build
```

## License

[Insert License Information]

## Contributing

[Insert Contributing Guidelines]
