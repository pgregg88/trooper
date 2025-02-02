"""Package setup for Stormtrooper Voice Assistant."""

from setuptools import setup, find_packages

setup(
    name="trooper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "boto3>=1.26.0",
        "python-dotenv>=0.19.0",
        "loguru>=0.7.0",
        "pydub>=0.25.1",
        "sounddevice>=0.4.6",
        "soundfile>=0.12.1",
    ],
    entry_points={
        "console_scripts": [
            "trooper=cli:main",
        ],
    },
) 