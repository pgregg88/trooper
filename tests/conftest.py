"""Pytest configuration and fixtures."""

import os
import pytest
from pathlib import Path
from typing import Generator
import soundfile as sf
import numpy as np
from dotenv import load_dotenv

# Load test environment variables
load_dotenv(".env.test", override=True)

@pytest.fixture
def test_audio_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a test audio file.
    
    Args:
        tmp_path: Pytest temporary directory fixture
        
    Yields:
        Path to test audio file
    """
    # Create a simple sine wave
    duration = 1.0  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    data = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
    
    # Save as WAV file
    file_path = tmp_path / "test_audio.wav"
    sf.write(file_path, data, sample_rate)
    
    yield file_path
    
    # Cleanup
    file_path.unlink(missing_ok=True)

@pytest.fixture
def mock_aws_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock AWS credentials for testing.
    
    Args:
        monkeypatch: Pytest monkeypatch fixture
    """
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")

@pytest.fixture
def test_config_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary config directory.
    
    Args:
        tmp_path: Pytest temporary directory fixture
        
    Yields:
        Path to test config directory
    """
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    yield config_dir
    
    # Cleanup
    for file in config_dir.glob("*"):
        file.unlink()
    config_dir.rmdir() 