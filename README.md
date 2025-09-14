# 🧘 Guided Meditation Generator

A simple and powerful Python application for creating personalized guided meditation audio files with background music and professional-quality text-to-speech.

## ✨ Features

- 🎤 **Multiple TTS Options**: Google TTS (high-quality) and local Windows TTS
- 🎵 **Background Music**: Automatic mixing with voice narration
- 🎛️ **Voice Controls**: Adjustable speech rate (80-200 WPM) and volume
- ⏸️ **Pause Commands**: Add natural pauses with `[PAUSE:X]` syntax
- 🎯 **Voice Testing**: Test voices before generating full meditation
- 📁 **Multiple Formats**: Supports MP3, WAV, OGG background music
- 🧘 **Sample Content**: Includes professional meditation template

## 🚀 Quick Start

### Basic Installation
```bash
pip install -r requirements.txt
python run.py
```

### With FFmpeg (for MP3 support)
```bash
conda env create -f environment.yml
conda activate meditation_generator
python run.py
```

### Manual FFmpeg Installation
- **Windows**: `choco install ffmpeg`
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## 📁 Project Structure

```
Generate Guided Meditation/
├── src/
│   └── meditation_generator.py    # Main application code
├── background_music/              # Place your background music here
│   └── README.txt                 # Instructions for background music
├── output/                       # Generated meditation files appear here
├── tests/                        # Test files
├── run.py                        # Entry point - run this!
├── requirements.txt              # Dependencies list
├── environment.yml               # Conda environment with FFmpeg
└── README.md                     # Complete documentation
```

## ✨ Features Working Perfectly

### Core Functionality
- ✅ **Volume Slider**: Controls voice volume (affects output files)
- ✅ **Rate Slider**: Controls speech speed 80-200 WPM (affects output files)
- ✅ **Google TTS**: High-quality internet-based text-to-speech
- ✅ **Local TTS**: Offline Windows text-to-speech
- ✅ **Background Music**: Automatic mixing with voice
- ✅ **Voice Testing**: Test voices before generation
- ✅ **Pause Commands**: Use [PAUSE:X] for X second pauses
- ✅ **Beautiful UI**: Clean interface with emoji indicators

### Audio Processing
- ✅ **Speed Adjustment**: Real-time audio speed modification
- ✅ **Volume Control**: Precise decibel-level adjustments
- ✅ **Music Looping**: Background music loops automatically if needed
- ✅ **File Cleanup**: Temporary files cleaned after generation
- ✅ **Multiple Formats**: Supports MP3, WAV, OGG background music

## 🎤 Voice Quality Guide

### Better Voice Options

#### Windows Store Voices
1. Open Microsoft Store
2. Search "Microsoft Speech Platform"
3. Install: Zira Mobile, Hazel, Eva Mobile, Aria

#### Windows Neural Voices (Windows 11)
1. Settings → Accessibility → Narrator → Voice
2. Download neural voices for higher quality

#### Google TTS (Built-in)
- Select "⭐ Google TTS" in the app
- Higher quality than local voices
- Multiple accents available
- Requires internet connection

### Voice Settings
- **Rate**: 100-120 WPM (slower = more natural for meditation)
- **Volume**: 70-85% (gentler, more soothing)
- **Voice**: Female voices typically sound softer for meditation

### Tips for Better Audio
- Use commas for natural pauses in speech
- Write shorter sentences for better TTS pronunciation
- Test voices with the "Test Voice" button before generating
- Use `[PAUSE:X]` commands for meditation-specific timing

## 🛠️ Troubleshooting

- **No audio output**: Check system audio settings and volume
- **TTS issues**: Try `pip install --upgrade pyttsx3`
- **FFmpeg warnings**: Install FFmpeg or use WAV files only
- **Voice not working**: Try different voice selection or restart app
- **Background music not mixing**: Ensure music file is in supported format

## 📦 Dependencies

Install with:
```bash
pip install -r requirements.txt
```

Required packages:
- `pyttsx3==2.90` - Local text-to-speech
- `pygame==2.5.2` - Audio playback and processing
- `pydub==0.25.1` - Audio manipulation
- `gtts==2.5.4` - Google Text-to-Speech

## 🎛️ Usage Guide

1. **Start the app**: `python run.py`
2. **Add background music**: Place MP3/WAV files in `background_music/` folder
3. **Select music**: Click Browse and choose your background track
4. **Write meditation**: Edit the text area or use the provided sample
5. **Adjust settings**: Use sliders to control voice rate and volume
6. **Choose voice**: Select TTS engine and voice accent
7. **Test voice**: Click "Test Voice" to hear your selection
8. **Generate**: Click "Create Meditation File"
9. **Find output**: Check the `output/` folder for your meditation file

## 🎯 Example Output

When you run the application, you'll see beautiful console output like:
```
🎤 Available voices:
✅ Selected female voice: Microsoft Zira Desktop
🎵 Voice settings: Rate=120 WPM, Volume=85%
✅ Google TTS detected and available
🎯 Starting meditation generation...
💪 Adjusting speech speed: 156 WPM -> 1.30x speed
✅ Final meditation created successfully!
📁 File: output/complete_meditation_20250913_194616.wav
🎉 Meditation generation complete!
```

## 📝 Sample Usage

The app comes with a complete sample meditation text that demonstrates:
- Natural breathing guidance
- Progressive relaxation techniques  
- Mindfulness instructions
- Proper use of pause commands
- Professional meditation structure

## 🔧 Customization

- **Meditation Text**: Edit directly in the GUI text area
- **Pause Commands**: Use `[PAUSE:5]` for 5-second pauses
- **Voice Settings**: Adjust rate (80-200 WPM) and volume (10-100%)
- **Background Music**: Any audio file that pydub can read
- **Output Quality**: High-quality WAV files with background music mixed

## 🚀 Getting Started

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Run the application**: `python run.py`
3. **Add background music**: Place audio files in `background_music/` folder
4. **Create your meditation**: Edit the text or use the sample provided
5. **Adjust settings**: Use sliders for voice rate and volume
6. **Test your voice**: Click "Test Voice" to preview
7. **Generate**: Click "Create Meditation File"
8. **Enjoy**: Find your meditation in the `output/` folder

## 🎆 Ready to Create Amazing Meditations!

Your meditation generator is ready to create professional-quality guided meditations with beautiful background music and natural-sounding speech. Perfect for personal use, sharing with friends, or developing your own meditation practice.

Happy meditating! 🧘‍♀️✨
