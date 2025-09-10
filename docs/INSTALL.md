# Installation Guide

## Quick Install
```bash
pip install -r requirements.txt
python run.py
```

## With FFmpeg (for MP3 support)
```bash
conda env create -f environment.yml
conda activate meditation_generator
python run.py
```

## Manual FFmpeg Install
- **Windows**: `choco install ffmpeg`
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## Troubleshooting
- **No audio**: Check system audio settings
- **TTS issues**: `pip install pyttsx3`
- **FFmpeg warning**: Install ffmpeg or use WAV files only