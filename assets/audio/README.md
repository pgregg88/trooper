# Audio Processing Directory

This directory contains audio files and processing scripts for the Stormtrooper voice effect system.

## Directory Structure

- `polly_raw/`: Original voice samples generated from Amazon Polly
- `processed/`: Voice samples with Stormtrooper effects applied
- `samples/`: Additional audio samples and templates

## File Naming Convention

- Original Polly files: `{Voice}_{Engine}_{Type}_{Category}.mp3`
  Example: `Stephen_neural_taunt_authority.mp3`

- Processed files: `{Original_Name}_processed.mp3`
  Example: `Stephen_neural_taunt_authority_processed.mp3`

## Processing Workflow

1. Place original Polly-generated audio files in the `polly_raw/` directory
2. Run `python src/audio/process_samples.py` to apply Stormtrooper effects
3. Processed files will be saved in the `processed/` directory
4. Use `python src/audio/play_samples.py` to compare original and processed samples

## Effect Chain

The Stormtrooper voice effect applies the following processing in order:

1. Noise Gate (-40dB threshold)
2. High-Pass Filter (500Hz)
3. Low-Pass Filter (2000Hz)
4. Hard Limiter (-6dB threshold)
5. Radio Effect (noise + interference)
6. Short Echo (20ms delay)
