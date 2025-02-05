"""Setup file for Stormtrooper Voice Assistant."""

from setuptools import setup, find_packages

setup(
    name="trooper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "soundfile",
        "sounddevice",
        "loguru",
        "pyyaml",
        "boto3",  # For Amazon Polly
    ],
    entry_points={
        "console_scripts": [
            "trooper=src.cli.trooper:main",
        ],
    },
    python_requires=">=3.8",
    description="Stormtrooper Voice Assistant with motion detection and audio effects",
    author="Your Name",
    author_email="your.email@example.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
