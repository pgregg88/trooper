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
        "loguru",
        "pyyaml"
    ],
    python_requires=">=3.8",
    description="Stormtrooper Voice Assistant with motion detection and audio effects",
    author="Your Name",
    author_email="your.email@example.com",
)
