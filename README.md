# 🧘 Guided Meditation Generator

Create personalized guided meditations with background music and natural text-to-speech.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

## Features

- **Natural TTS**: Google TTS and local voices
- **Background Music**: Automatic looping
- **Pause Control**: Add `[PAUSE:X]` for X-second pauses
- **Voice Customization**: Rate, volume, and voice selection
- **Clean Output**: Only final meditation file remains

## Usage

1. **Add music**: Place MP3/WAV files in `background_music/` folder
2. **Write meditation**: Use `[PAUSE:5]` for 5-second pauses
3. **Generate**: Click "Generate Meditation"
4. **Find output**: Check `output/` folder for final file

## Example Script

```
Welcome to this peaceful meditation.

[PAUSE:3]

Take three deep breaths.

[PAUSE:5]

Feel your body relaxing.
```

## Requirements

- Python 3.8+
- `pyttsx3`, `pygame`, `pydub`, `gtts`

## Installation Options

- **Basic**: `pip install -r requirements.txt`
- **With FFmpeg**: `conda env create -f environment.yml`
- **Manual**: See `docs/INSTALL.md`

---

**Enjoy your personalized meditation! 🧘‍♀️🎵**