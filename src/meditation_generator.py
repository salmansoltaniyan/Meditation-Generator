#!/usr/bin/env python3
"""
Guided Meditation Generator
A Python application to create guided meditations with background music,
natural voice synthesis, and pause functionality.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pyttsx3
import pygame
import time
import os
import re
from pathlib import Path
import tempfile
import wave


class MeditationGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Guided Meditation Generator")
        self.root.geometry("800x900")  # Increased height from 700 to 900
        self.root.configure(bg='#2E3440')
        self.root.minsize(800, 850)  # Set minimum size to prevent too small window
        
        # Initialize TTS engine
        try:
            self.tts_engine = pyttsx3.init()
            self.setup_voice()
            self.tts_working = True
        except Exception as e:
            print(f"TTS initialization failed: {e}")
            self.tts_engine = None
            self.tts_working = False
        
        # Initialize pygame mixer for audio
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Variables
        self.background_music_file = tk.StringVar()
        self.meditation_text = tk.StringVar()
        self.is_playing = False
        self.is_paused = False
        self.background_music = None
        self.generated_audio_files = []
        
        self.setup_ui()
        self.create_background_music_folder()
    
    def setup_voice(self):
        """Configure TTS engine for natural, soft voice"""
        if not self.tts_engine:
            return
            
        voices = self.tts_engine.getProperty('voices')
        
        # Enhanced female voice detection with more keywords
        female_voice = None
        best_quality_voice = None
        
        print("🎤 Available voices:")
        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.name}")
            
            voice_name_lower = voice.name.lower()
            
            # Look for high-quality female voices first
            if any(keyword in voice_name_lower for keyword in [
                'zira', 'hazel', 'eva', 'aria', 'cortana', 'susan', 'mary', 'helen',
                'female', 'woman', 'natural', 'neural', 'premium'
            ]):
                if not female_voice or 'neural' in voice_name_lower or 'premium' in voice_name_lower:
                    female_voice = voice
                    if 'neural' in voice_name_lower or 'premium' in voice_name_lower:
                        best_quality_voice = voice
        
        # Select the best available voice
        if best_quality_voice:
            selected_voice = best_quality_voice
            print(f"✅ Selected high-quality voice: {selected_voice.name}")
        elif female_voice:
            selected_voice = female_voice
            print(f"✅ Selected female voice: {selected_voice.name}")
        elif voices:
            selected_voice = voices[0]
            print(f"⚠️ Using default voice: {selected_voice.name}")
        else:
            print("❌ No voices available")
            return
        
        self.tts_engine.setProperty('voice', selected_voice.id)
        
        # Optimized settings for meditation (slower, softer)
        self.tts_engine.setProperty('rate', 120)  # Slower for meditation
        self.tts_engine.setProperty('volume', 0.85)  # Slightly softer
        
        print(f"🎵 Voice settings: Rate=120 WPM, Volume=85%")
    
    def populate_engine_options(self):
        """Populate the TTS engine selection dropdown"""
        engines = ["Local TTS (pyttsx3)"]
        
        # Check for gTTS
        try:
            import gtts
            engines.append("⭐ Google TTS (gTTS) - High Quality")
            print("✅ Google TTS detected and available")
        except ImportError as e:
            engines.append("Google TTS (gTTS) - Not Installed")
            print(f"❌ Google TTS not available: {e}")
        
        self.engine_combo['values'] = engines
        
        # Default to Google TTS if available, otherwise local
        if any("Google TTS (gTTS) - High Quality" in engine for engine in engines):
            for i, engine in enumerate(engines):
                if "Google TTS (gTTS) - High Quality" in engine:
                    self.engine_combo.current(i)
                    print(f"🎯 Defaulting to Google TTS (index {i})")
                    break
        else:
            self.engine_combo.current(0)  # Default to local TTS
            print("🎯 Defaulting to Local TTS")
    
    def on_engine_changed(self, event=None):
        """Handle TTS engine selection change"""
        self.populate_voice_options()
    
    def get_selected_engine(self):
        """Get the currently selected TTS engine"""
        selected = self.engine_var.get()
        if "Google TTS" in selected and "High Quality" in selected:
            return "gtts"
        else:
            return "pyttsx3"
    
    def populate_voice_options(self):
        """Populate the voice selection dropdown based on selected engine"""
        selected_engine = self.get_selected_engine()
        
        if selected_engine == "gtts":
            # Google TTS options - 7 different accents
            voice_options = [
                "🌸 English (US Female, Slow) - BEST for Meditation",
                "🗣️ English (US Standard Speed)",
                "🇬🇧 British English (Slow) - Elegant",
                "🇦🇺 Australian English (Slow) - Warm",
                "🇮🇳 Indian English (Slow) - Clear",
                "🇨🇦 Canadian English (Slow) - Neutral",
                "🇿🇦 South African English (Slow) - Distinctive"
            ]
            self.voice_combo['values'] = voice_options
            self.voice_combo.current(0)  # Default to best for meditation
            
        else:
            # Local pyttsx3 voices
            if not self.tts_working or not self.tts_engine:
                self.voice_combo['values'] = ["No TTS engine available"]
                self.voice_var.set("No TTS engine available")
                return
                
            try:
                voices = self.tts_engine.getProperty('voices')
                voice_options = []
                selected_index = 0
                
                for i, voice in enumerate(voices):
                    # Create readable voice names
                    display_name = voice.name
                    if len(display_name) > 50:
                        display_name = display_name[:47] + "..."
                    
                    # Mark recommended voices
                    voice_lower = voice.name.lower()
                    if any(keyword in voice_lower for keyword in ['neural', 'premium', 'natural']):
                        display_name = f"⭐ {display_name}"
                    elif any(keyword in voice_lower for keyword in ['zira', 'hazel', 'eva', 'aria', 'female', 'woman']):
                        display_name = f"🌸 {display_name}"
                        if not any("⭐" in opt for opt in voice_options):  # Select first female if no premium
                            selected_index = i
                    
                    voice_options.append(display_name)
                
                self.voice_combo['values'] = voice_options
                if voice_options:
                    self.voice_combo.current(selected_index)
                    
            except Exception as e:
                print(f"Error populating voices: {e}")
                self.voice_combo['values'] = ["Error loading voices"]
                self.voice_var.set("Error loading voices")
    
    def test_selected_voice(self):
        """Test the currently selected voice"""
        selected_engine = self.get_selected_engine()
        
        if selected_engine == "gtts":
            self.test_google_voice()
        else:
            self.test_local_voice()
    
    def test_google_voice(self):
        """Test Google TTS voice"""
        try:
            from gtts import gTTS
            import tempfile
            import os
            
            selected_voice = self.voice_var.get()
            test_text = "Welcome to this guided meditation. Take a deep breath and feel yourself relaxing."
            
            print(f"🎤 Testing Google TTS voice: {selected_voice}")
            
            # Determine settings based on voice selection
            if "British" in selected_voice:
                lang = 'en'
                tld = 'co.uk'
            elif "Australian" in selected_voice:
                lang = 'en'
                tld = 'com.au'
            elif "Indian" in selected_voice:
                lang = 'en'
                tld = 'co.in'
            elif "Canadian" in selected_voice:
                lang = 'en'
                tld = 'ca'
            elif "South African" in selected_voice:
                lang = 'en'
                tld = 'co.za'
            else:
                lang = 'en'
                tld = 'com'
            
            slow = "Slow" in selected_voice or "Female" in selected_voice
            
            print(f"🌐 Google TTS settings: lang={lang}, tld={tld}, slow={slow}")
            
            # Create TTS
            tts = gTTS(text=test_text, lang=lang, slow=slow, tld=tld)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_filename = temp_file.name
            
            tts.save(temp_filename)
            
            # Try to play the file
            try:
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                pygame.mixer.quit()
                
            except Exception as play_error:
                print(f"⚠️ Could not play audio: {play_error}")
                print(f"✅ Audio file created: {temp_filename}")
                print("🎧 You can play this file manually to hear the voice")
            
            # Clean up
            try:
                os.unlink(temp_filename)
            except:
                pass
                
        except Exception as e:
            messagebox.showerror("Google TTS Test Error", f"Error testing Google TTS voice: {str(e)}")
    
    def test_local_voice(self):
        """Test local TTS voice"""
        if not self.tts_working or not self.tts_engine:
            messagebox.showwarning("No TTS", "Text-to-speech engine not available")
            return
            
        try:
            voices = self.tts_engine.getProperty('voices')
            selected_index = self.voice_combo.current()
            
            if 0 <= selected_index < len(voices):
                selected_voice = voices[selected_index]
                
                # Apply current settings
                self.tts_engine.setProperty('voice', selected_voice.id)
                self.tts_engine.setProperty('rate', self.rate_var.get())
                self.tts_engine.setProperty('volume', self.volume_var.get())
                
                test_text = "Welcome to this guided meditation. Take a deep breath and feel yourself relaxing."
                
                print(f"🎤 Testing local voice: {selected_voice.name}")
                print(f"   Rate: {self.rate_var.get()} WPM, Volume: {self.volume_var.get():.1f}")
                
                self.tts_engine.say(test_text)
                self.tts_engine.runAndWait()
                
            else:
                messagebox.showwarning("Invalid Selection", "Please select a valid voice")
                
        except Exception as e:
            messagebox.showerror("Voice Test Error", f"Error testing voice: {str(e)}")
    
    def get_selected_voice_id(self):
        """Get the ID of the currently selected voice"""
        if not self.tts_working or not self.tts_engine:
            return None
            
        try:
            voices = self.tts_engine.getProperty('voices')
            selected_index = self.voice_combo.current()
            
            if 0 <= selected_index < len(voices):
                return voices[selected_index].id
            return None
            
        except:
            return None
    
    def create_background_music_folder(self):
        """Create background music folder if it doesn't exist"""
        music_dir = Path("background_music")
        music_dir.mkdir(exist_ok=True)
        
        # Create a sample info file
        info_file = music_dir / "README.txt"
        if not info_file.exists():
            info_file.write_text(
                "Place your background music files (.mp3, .wav, .ogg) in this folder.\n"
                "Recommended: Soft instrumental music, nature sounds, or ambient tracks.\n"
                "Files should be at least as long as your meditation session."
            )
    
    def setup_ui(self):
        """Create the user interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for dark theme
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#2E3440', foreground='#ECEFF4')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), background='#2E3440', foreground='#ECEFF4')
        style.configure('Custom.TLabel', background='#2E3440', foreground='#ECEFF4')
        style.configure('Custom.TButton', font=('Arial', 10))
        
        # Main title
        title_label = ttk.Label(self.root, text="Guided Meditation Generator", style='Title.TLabel')
        title_label.pack(pady=(20, 30))
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Background music selection
        music_frame = ttk.LabelFrame(main_frame, text="Background Music", padding=15)
        music_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(music_frame, text="Select background music:", style='Custom.TLabel').pack(anchor='w')
        
        music_select_frame = ttk.Frame(music_frame)
        music_select_frame.pack(fill='x', pady=(5, 0))
        
        self.music_entry = ttk.Entry(music_select_frame, textvariable=self.background_music_file, state='readonly')
        self.music_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        ttk.Button(music_select_frame, text="Browse", command=self.browse_music, style='Custom.TButton').pack(side='right')
        
        # Meditation text input
        text_frame = ttk.LabelFrame(main_frame, text="Meditation Script", padding=15)
        text_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        ttk.Label(text_frame, text="Enter your meditation text (use [pause:X] for X second pauses):", style='Custom.TLabel').pack(anchor='w')
        
        # Text area with scrollbar (reduced height to fit all controls)
        self.text_area = scrolledtext.ScrolledText(
            text_frame, 
            wrap=tk.WORD, 
            height=10, 
            font=('Arial', 11),
            bg='#3B4252',
            fg='#ECEFF4',
            insertbackground='#ECEFF4',
            relief='flat',
            borderwidth=1
        )
        self.text_area.pack(fill='both', expand=True, pady=(5, 0))
        
        # Load sample meditation text (inline)
        sample_text = """Welcome.
Find a comfortable position, either seated or lying down.
Allow your body to settle.
Close your eyes gently.
[PAUSE:5]

Take a slow, deep breath in through the nose.
Let the breath travel all the way down into the belly.
[PAUSE:4]

Exhale slowly through the mouth, releasing any tension.
[PAUSE:5]

Again—inhale slowly through the nose.
Feel the chest rise.
Feel the belly expand.
[PAUSE:4]

Exhale gently, letting the body soften.
[PAUSE:6]

Now, allow your breathing to find its natural rhythm.
Simply notice each inhale[EMOJI]
and each exhale.
[PAUSE:8]

As you breathe in, feel the coolness of the air at the tip of your nose.
As you breathe out, notice the warmth leaving your body.
[PAUSE:8]

Your breath is an anchor.
Always here.
Always steady.
[PAUSE:8]

If thoughts arise, let them drift by—like clouds in the sky.
Gently return your attention to the breath.
Inhale…
Exhale…
[PAUSE:10]

Feel the body supported by the ground beneath you.
No need to hold on to anything.
Just breathing.
Just being.
[PAUSE:10]

Notice the slight pause at the top of each inhale.
A stillness…
a space.
[PAUSE:6]

Notice the pause at the end of each exhale.
Another space.
Another moment of quiet.
[PAUSE:8]

Breathing in—new energy enters the body.
Breathing out—release, and let go.
[PAUSE:10]

Now, bring your attention to the rise and fall of the belly.
With each inhale, the belly expands.
With each exhale, it softens.
[PAUSE:8]

Stay with this gentle rhythm.
Breathing in calm…
Breathing out ease.
[PAUSE:12]

If the mind wanders, it's okay.
Softly bring it back to the breath.
Inhale…
Exhale…
[PAUSE:12]

Let your breath slow even more.
Inhale… count silently to four.
One… two… three… four.
[PAUSE:4]

Exhale… count silently to six.
One… two… three… four… five… six.
[PAUSE:6]

Continue this rhythm for a few rounds.
[PAUSE:20]

Now, let go of the counting.
Return to simply watching the breath.
Natural.
Effortless.
[PAUSE:12]

Feel the body at ease.
The mind calm.
The breath steady.
[PAUSE:12]

Take a final deep breath in—filling the lungs completely.
Hold it for a moment.
[PAUSE:4]

And exhale fully, releasing everything.
[PAUSE:8]

When you're ready, gently wiggle your fingers and toes.
Slowly bring awareness back to your surroundings.
[PAUSE:6]

Take one last soft breath in…
and out.
[PAUSE:6]

When it feels right, open your eyes.
Your meditation is complete.
[PAUSE:4]"""
        
        # Insert the sample text into the text area
        self.text_area.insert('1.0', sample_text)
        print("✅ Loaded inline sample meditation text")
        
        # Voice settings
        voice_frame = ttk.LabelFrame(main_frame, text="Voice Settings", padding=15)
        voice_frame.pack(fill='x', pady=(0, 15))
        
        # TTS Engine selection
        engine_select_frame = ttk.Frame(voice_frame)
        engine_select_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(engine_select_frame, text="TTS Engine:", style='Custom.TLabel').pack(side='left')
        self.engine_var = tk.StringVar()
        self.engine_combo = ttk.Combobox(engine_select_frame, textvariable=self.engine_var, state='readonly', width=25)
        self.engine_combo.pack(side='left', padx=(10, 10))
        self.engine_combo.bind('<<ComboboxSelected>>', self.on_engine_changed)
        
        # Voice selection
        voice_select_frame = ttk.Frame(voice_frame)
        voice_select_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(voice_select_frame, text="Voice:", style='Custom.TLabel').pack(side='left')
        self.voice_var = tk.StringVar()
        self.voice_combo = ttk.Combobox(voice_select_frame, textvariable=self.voice_var, state='readonly', width=40)
        self.voice_combo.pack(side='left', padx=(10, 10))
        
        ttk.Button(voice_select_frame, text="Test Voice", command=self.test_selected_voice, style='Custom.TButton').pack(side='left')
        
        # Populate engine and voice options
        self.populate_engine_options()
        self.populate_voice_options()
        
        # TTS Voice Controls Section
        voice_controls = ttk.Frame(voice_frame)
        voice_controls.pack(fill='x', pady=(10, 0))
        
        # Add a separator line for clarity
        separator = ttk.Separator(voice_frame, orient='horizontal')
        separator.pack(fill='x', pady=(5, 10))
        
        # Speech rate with clear labeling
        rate_frame = ttk.Frame(voice_controls)
        rate_frame.pack(side='left', padx=(0, 30))
        
        ttk.Label(rate_frame, text="Voice Speech Rate (WPM):", style='Custom.TLabel').pack(anchor='w')
        self.rate_var = tk.IntVar(value=120)  # Slower default for meditation
        rate_scale = ttk.Scale(rate_frame, from_=80, to=200, variable=self.rate_var, orient='horizontal', length=150)
        rate_scale.pack(pady=(2, 0))
        
        # Rate value display
        self.rate_display = ttk.Label(rate_frame, text="120 WPM", style='Custom.TLabel')
        self.rate_display.pack()
        
        # Update rate display when slider changes
        def update_rate_display(value):
            val = int(float(value))
            self.rate_display.config(text=f"{val} WPM")
        rate_scale.configure(command=update_rate_display)
        
        # Volume with clear labeling
        volume_frame = ttk.Frame(voice_controls)
        volume_frame.pack(side='left')
        
        ttk.Label(volume_frame, text="Voice Volume Level:", style='Custom.TLabel').pack(anchor='w')
        self.volume_var = tk.DoubleVar(value=0.85)  # Softer default
        volume_scale = ttk.Scale(volume_frame, from_=0.1, to=1.0, variable=self.volume_var, orient='horizontal', length=150)
        volume_scale.pack(pady=(2, 0))
        
        # Volume value display
        self.volume_display = ttk.Label(volume_frame, text="85%", style='Custom.TLabel')
        self.volume_display.pack()
        
        # Update volume display when slider changes
        def update_volume_display(value):
            val = int(float(value) * 100)
            self.volume_display.config(text=f"{val}%")
        volume_scale.configure(command=update_volume_display)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(0, 10))
        
        self.generate_btn = ttk.Button(button_frame, text="Create Meditation File", command=self.generate_meditation, style='Custom.TButton')
        self.generate_btn.pack(side='left', padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="Cancel", command=self.stop_meditation, style='Custom.TButton', state='disabled')
        self.stop_btn.pack(side='left', padx=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to create your meditation file", style='Custom.TLabel')
        self.status_label.pack(pady=(10, 0))
    
    def browse_music(self):
        """Browse for background music file"""
        file_types = [
            ("Audio files", "*.mp3 *.wav *.ogg *.m4a"),
            ("MP3 files", "*.mp3"),
            ("WAV files", "*.wav"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Background Music",
            filetypes=file_types,
            initialdir="background_music"
        )
        
        if filename:
            self.background_music_file.set(filename)
    
    def parse_meditation_text(self, text):
        """Parse meditation text and extract pauses"""
        segments = []
        current_pos = 0
        
        # Find all pause markers (case-insensitive, flexible spacing)
        pause_pattern = r'\[pause\s*:\s*(\d+)\s*\]'
        matches = list(re.finditer(pause_pattern, text, re.IGNORECASE))
        
        for match in matches:
            # Add text before pause
            if match.start() > current_pos:
                text_segment = text[current_pos:match.start()].strip()
                if text_segment:
                    segments.append(('text', text_segment))
            
            # Add pause
            pause_duration = int(match.group(1))
            segments.append(('pause', pause_duration))
            current_pos = match.end()
        
        # Add remaining text
        if current_pos < len(text):
            remaining_text = text[current_pos:].strip()
            if remaining_text:
                segments.append(('text', remaining_text))
        
        return segments
    
    def estimate_meditation_duration(self, segments):
        """Estimate total duration of meditation in seconds"""
        total_duration = 0
        speech_rate = self.rate_var.get()  # words per minute
        
        for segment_type, content in segments:
            if segment_type == 'text':
                # Estimate speech duration based on word count and speech rate
                word_count = len(content.split())
                speech_duration = (word_count / speech_rate) * 60  # convert to seconds
                total_duration += speech_duration
            elif segment_type == 'pause':
                total_duration += content
        
        return total_duration
    
    def get_audio_duration(self, audio_file):
        """Get duration of audio file in seconds"""
        try:
            # Load the audio file to get its length
            sound = pygame.mixer.Sound(audio_file)
            duration = sound.get_length()
            return duration
        except:
            # If we can't get duration, return a default that will trigger looping
            return 60  # 1 minute default
    
    def manage_background_music(self, meditation_duration):
        """Display information about background music (no longer used for playback)"""
        if not self.background_music_file.get():
            return
        
        try:
            music_duration = self.get_audio_duration(self.background_music_file.get())
            
            # Just display information, no actual playback
            minutes = int(meditation_duration // 60)
            seconds = int(meditation_duration % 60)
            music_mins = int(music_duration // 60)
            music_secs = int(music_duration % 60)
            
            if music_duration < meditation_duration:
                print(f"🔄 Background music will loop (Meditation: {minutes}:{seconds:02d}, Music: {music_mins}:{music_secs:02d})")
            else:
                print(f"🎼 Background music covers full meditation (Meditation: {minutes}:{seconds:02d}, Music: {music_mins}:{music_secs:02d})")
                
        except Exception as e:
            print(f"Warning: Could not analyze background music: {e}")
    
    def text_to_speech_file(self, text, filename):
        """Convert text to speech and save as file with selected engine"""
        print(f"🎤 Starting TTS for: {text[:50]}...")
        
        selected_engine = self.get_selected_engine()
        
        if selected_engine == "gtts":
            return self.create_speech_gtts(text, filename)
        else:
            return self.create_speech_pyttsx3(text, filename)
    
    def create_speech_gtts(self, text, filename):
        """Create speech using Google TTS"""
        try:
            from gtts import gTTS
            import os
            
            # Get voice settings from selection
            selected_voice = self.voice_var.get()
            
            # Get rate and volume from sliders
            rate_setting = self.rate_var.get()
            volume_setting = self.volume_var.get()
            
            print(f"🎛️ TTS Settings from sliders: Rate={rate_setting} WPM, Volume={volume_setting:.1f}")
            
            # Determine language and slow setting based on voice selection
            if "British" in selected_voice:
                lang = 'en'
                tld = 'co.uk'
            elif "Australian" in selected_voice:
                lang = 'en'
                tld = 'com.au'
            elif "Indian" in selected_voice:
                lang = 'en'
                tld = 'co.in'
            elif "Canadian" in selected_voice:
                lang = 'en'
                tld = 'ca'
            elif "South African" in selected_voice:
                lang = 'en'
                tld = 'co.za'
            else:
                lang = 'en'
                tld = 'com'  # Default to US English
            
            # Determine slow setting based on both voice selection AND rate slider
            # If rate is below 150 WPM, use slow speech
            slow = ("Slow" in selected_voice or "Female" in selected_voice) or (rate_setting < 150)
            
            print(f"🌐 Using Google TTS: lang={lang}, tld={tld}, slow={slow} (based on rate={rate_setting})")
            
            # Create TTS
            tts = gTTS(text=text, lang=lang, slow=slow, tld=tld)
            
            # Save as MP3 first, then convert to WAV if needed
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_mp3 = temp_file.name
            
            tts.save(temp_mp3)
            
            # Convert MP3 to WAV and adjust volume using pydub if available
            try:
                from pydub import AudioSegment
                audio = AudioSegment.from_mp3(temp_mp3)
                
                # Adjust speed based on rate slider setting
                # Convert rate (80-200 WPM) to speed multiplier
                # 120 WPM (default) = 1.0x speed, lower = slower, higher = faster
                default_rate = 120  # Default meditation rate
                if rate_setting != default_rate:
                    # Calculate speed multiplier (0.5x to 1.8x)
                    speed_multiplier = rate_setting / default_rate
                    # Clamp to reasonable range
                    speed_multiplier = max(0.5, min(speed_multiplier, 1.8))
                    
                    print(f"💪 Adjusting speech speed: {rate_setting} WPM -> {speed_multiplier:.2f}x speed")
                    
                    # Change speed by adjusting frame rate
                    # Higher frame rate = faster playback
                    original_frame_rate = audio.frame_rate
                    new_frame_rate = int(original_frame_rate * speed_multiplier)
                    audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})
                    # Convert back to original sample rate to maintain pitch
                    audio = audio.set_frame_rate(original_frame_rate)
                    
                    print(f"✅ Speed adjusted: {original_frame_rate}Hz -> {new_frame_rate}Hz -> {original_frame_rate}Hz")
                
                # Adjust volume based on slider setting
                # Convert volume (0.1-1.0) to decibels
                # 0.85 (default) = 0dB, lower values = negative dB, higher = positive dB
                if volume_setting != 0.85:  # Only adjust if different from default
                    volume_db = 20 * (volume_setting - 0.85) / 0.75  # Scale to reasonable dB range
                    audio = audio + volume_db
                    print(f"🔊 Volume adjusted by {volume_db:.1f}dB (slider: {volume_setting:.2f})")
                
                audio.export(filename, format="wav")
                os.unlink(temp_mp3)  # Remove temporary MP3
                print(f"✅ Google TTS created: {filename}")
            except Exception as e:
                # If pydub fails, just rename MP3 to WAV (will work for final mixing)
                import shutil
                shutil.move(temp_mp3, filename)
                print(f"✅ Google TTS created: {filename} (as MP3, pydub failed: {e})")
                print(f"⚠️ Speed and volume adjustments not applied due to pydub failure")
            
            return True
            
        except Exception as e:
            print(f"❌ Google TTS failed: {e}")
            print("🔄 Falling back to local TTS...")
            return self.create_speech_pyttsx3(text, filename)
    
    def create_speech_pyttsx3(self, text, filename):
        """Create speech using local pyttsx3 engine"""
        rate_setting = self.rate_var.get()
        volume_setting = self.volume_var.get()
        
        print(f"🎤 Using local TTS engine...")
        print(f"🎛️ TTS Settings from sliders: Rate={rate_setting} WPM, Volume={volume_setting:.2f}")
        
        # Create a fresh TTS engine for each segment to avoid conflicts
        try:
            import pyttsx3
            fresh_engine = pyttsx3.init()
            fresh_engine.setProperty('rate', rate_setting)
            fresh_engine.setProperty('volume', volume_setting)
            
            print(f"✅ Fresh TTS engine created with Rate={rate_setting}, Volume={volume_setting:.2f}")
            
        except Exception as e:
            print(f"❌ Failed to create fresh TTS engine: {e}")
            print("🔇 Creating silent audio as fallback")
            self._create_silent_audio(filename, duration=len(text.split()) * 0.5)
            return
            
        # Use a simple subprocess approach for maximum reliability
        try:
            import subprocess
            import sys
            import os
            
            # Create a simple TTS script that runs in isolation
            # Escape text properly for the script
            escaped_text = text.replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
            # Convert Windows path to forward slashes (Python handles this fine)
            normalized_filename = filename.replace('\\', '/')
            
            # Get selected voice ID
            selected_voice_id = self.get_selected_voice_id()
            voice_setup = ""
            if selected_voice_id:
                # Escape voice ID for script
                escaped_voice_id = selected_voice_id.replace('\\', '\\\\').replace('"', '\\"')
                voice_setup = f'    engine.setProperty("voice", "{escaped_voice_id}")'
            
            tts_script = f'''
import pyttsx3
import sys
import os

try:
    engine = pyttsx3.init()
{voice_setup}
    engine.setProperty('rate', {rate_setting})
    engine.setProperty('volume', {volume_setting})
    print(f"TTS Script: Rate={{rate_setting}}, Volume={{volume_setting}}")
    engine.save_to_file("""{escaped_text}""", "{normalized_filename}")
    engine.runAndWait()
    print("TTS_SUCCESS")
except Exception as e:
    print(f"TTS_ERROR: {{e}}")
    sys.exit(1)
'''
            
            # Write script to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as script_file:
                script_file.write(tts_script)
                script_filename = script_file.name
            
            try:
                # Run the TTS script with timeout
                print(f"🚀 Running isolated TTS process...")
                result = subprocess.run(
                    [sys.executable, script_filename],
                    capture_output=True,
                    text=True,
                    timeout=20  # 20 second timeout
                )
                
                if result.returncode == 0 and "TTS_SUCCESS" in result.stdout:
                    print("✅ TTS generation completed successfully")
                    # Verify file was created
                    if os.path.exists(filename) and os.path.getsize(filename) > 0:
                        print(f"✅ Audio file created: {os.path.getsize(filename)} bytes")
                    else:
                        print("❌ Audio file not created, using fallback")
                        self._create_silent_audio(filename, duration=len(text.split()) * 0.5)
                else:
                    print(f"❌ TTS process failed: {result.stderr}")
                    self._create_silent_audio(filename, duration=len(text.split()) * 0.5)
                    
            except subprocess.TimeoutExpired:
                print("⏰ TTS process timeout - creating silent audio")
                self._create_silent_audio(filename, duration=len(text.split()) * 0.5)
            except Exception as e:
                print(f"❌ TTS subprocess error: {e}")
                self._create_silent_audio(filename, duration=len(text.split()) * 0.5)
            finally:
                # Clean up script file
                try:
                    os.unlink(script_filename)
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ TTS generation failed completely: {e}")
            # Final fallback - create silent audio
            self._create_silent_audio(filename, duration=len(text.split()) * 0.5)
    
    def _create_silent_audio(self, filename, duration=1.0):
        """Create a silent audio file as fallback"""
        import wave
        import struct
        
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample
            wav_file.setframerate(sample_rate)
            
            # Write silent frames
            for _ in range(frames):
                wav_file.writeframes(struct.pack('<h', 0))
    
    def create_final_meditation_file(self, audio_segments, estimated_duration):
        """Create a final meditation file combining voice and background music"""
        try:
            from pydub import AudioSegment
            import datetime
            
            print("🎵 Creating final meditation file with background music...")
            
            # Generate filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            final_filename = f"output/complete_meditation_{timestamp}.wav"
            
            # Load background music
            if not self.background_music_file.get():
                print("❌ No background music selected")
                return None
                
            print(f"🎼 Loading background music: {self.background_music_file.get()}")
            
            # Try different methods to load background music
            background = None
            music_file = self.background_music_file.get()
            
            try:
                # First try: Direct loading (works for WAV without ffmpeg)
                if music_file.lower().endswith('.wav'):
                    background = AudioSegment.from_wav(music_file)
                    print("✅ Loaded WAV background music successfully")
                else:
                    # For MP3/other formats, try with ffmpeg
                    background = AudioSegment.from_file(music_file)
                    print("✅ Loaded background music with ffmpeg")
            except Exception as e:
                print(f"❌ Failed to load background music: {e}")
                print("[EMOJI] Try converting your background music to WAV format")
                print("[EMOJI] Or install ffmpeg for MP3 support")
                return self.create_voice_only_file(audio_segments, final_filename)
            
            # Create the voice track by combining all segments
            print("🎤 Combining voice segments...")
            voice_track = AudioSegment.empty()
            
            for segment_type, content in audio_segments:
                if segment_type == 'audio':
                    if os.path.exists(content):
                        print(f"  Adding audio: {content}")
                        audio_segment = AudioSegment.from_wav(content)
                        voice_track += audio_segment
                    else:
                        print(f"  ⚠️ Missing audio file: {content}")
                        # Add silence instead
                        silence_duration = 2000  # 2 seconds
                        voice_track += AudioSegment.silent(duration=silence_duration)
                        
                elif segment_type == 'pause':
                    print(f"  Adding {content}s pause")
                    pause_duration = int(content * 1000)  # Convert to milliseconds
                    voice_track += AudioSegment.silent(duration=pause_duration)
            
            # Ensure background music is long enough
            voice_duration = len(voice_track)
            print(f"📊 Voice track duration: {voice_duration/1000:.1f}s")
            print(f"📊 Background music duration: {len(background)/1000:.1f}s")
            
            if len(background) < voice_duration:
                # Loop background music to cover the entire meditation
                loops_needed = (voice_duration // len(background)) + 1
                print(f"🔄 Looping background music {loops_needed} times")
                background = background * loops_needed
            
            # Trim background to match voice duration exactly
            background = background[:voice_duration]
            
            # Reduce background volume and mix with voice
            background = background - 12  # Reduce volume by 12dB (about 25% volume)
            
            print("🎚️ Mixing voice and background music...")
            # Overlay voice on background music
            final_mix = background.overlay(voice_track)
            
            # Export final file
            print(f"💾 Exporting final meditation: {final_filename}")
            final_mix.export(final_filename, format="wav")
            
            file_size = os.path.getsize(final_filename)
            duration_minutes = len(final_mix) / 60000
            
            print(f"✅ Final meditation created successfully!")
            print(f"📁 File: {final_filename}")
            print(f"📊 Size: {file_size:,} bytes")
            print(f"⏱️ Duration: {duration_minutes:.1f} minutes")
            
            return final_filename
            
        except ImportError:
            print("❌ pydub library required for creating final meditation file")
            print("[EMOJI] Install with: pip install pydub")
            return None
        except Exception as e:
            print(f"❌ Error creating final meditation file: {e}")
            return None
    
    def create_voice_only_file(self, audio_segments, filename):
        """Create a voice-only meditation file as fallback"""
        try:
            from pydub import AudioSegment
            
            print("🎤 Creating voice-only meditation file...")
            
            # Create the voice track by combining all segments
            voice_track = AudioSegment.empty()
            
            for segment_type, content in audio_segments:
                if segment_type == 'audio':
                    if os.path.exists(content):
                        print(f"  Adding audio: {content}")
                        audio_segment = AudioSegment.from_wav(content)
                        voice_track += audio_segment
                    else:
                        print(f"  ⚠️ Missing audio file: {content}")
                        # Add silence instead
                        silence_duration = 2000  # 2 seconds
                        voice_track += AudioSegment.silent(duration=silence_duration)
                        
                elif segment_type == 'pause':
                    print(f"  Adding {content}s pause")
                    pause_duration = int(content * 1000)  # Convert to milliseconds
                    voice_track += AudioSegment.silent(duration=pause_duration)
            
            # Export voice-only file
            voice_filename = filename.replace("complete_meditation_", "voice_only_meditation_")
            print(f"💾 Exporting voice-only meditation: {voice_filename}")
            voice_track.export(voice_filename, format="wav")
            
            file_size = os.path.getsize(voice_filename)
            duration_minutes = len(voice_track) / 60000
            
            print(f"✅ Voice-only meditation created successfully!")
            print(f"📁 File: {voice_filename}")
            print(f"📊 Size: {file_size:,} bytes")
            print(f"⏱️ Duration: {duration_minutes:.1f} minutes")
            print("[EMOJI] To add background music, convert your music file to WAV format or install ffmpeg")
            
            return voice_filename
            
        except Exception as e:
            print(f"❌ Error creating voice-only file: {e}")
            return None
    
    def cleanup_segment_files(self):
        """Clean up individual segment files after final file creation"""
        print("🧹 Cleaning up individual segment files...")
        cleaned_count = 0
        
        for segment_file in self.generated_audio_files:
            try:
                if os.path.exists(segment_file):
                    os.unlink(segment_file)
                    cleaned_count += 1
                    print(f"  🗑️ Removed: {segment_file}")
            except Exception as e:
                print(f"  ⚠️ Could not remove {segment_file}: {e}")
        
        if cleaned_count > 0:
            print(f"✅ Cleaned up {cleaned_count} segment file(s)")
        
        # Clear the list since files are deleted
        self.generated_audio_files.clear()
    
    def generate_meditation(self):
        """Generate and play the guided meditation"""
        if not self.background_music_file.get():
            messagebox.showwarning("No Music", "Please select background music first.")
            return
        
        meditation_text = self.text_area.get('1.0', tk.END).strip()
        if not meditation_text:
            messagebox.showwarning("No Text", "Please enter meditation text.")
            return
        
        # Disable generate button and enable cancel button
        self.generate_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        
        # Start progress bar
        self.progress.start()
        self.status_label.config(text="Generating meditation...")
        
        # Set is_playing to True at the start
        print(f"🎯 Setting is_playing to True (was: {self.is_playing})")
        self.is_playing = True
        print(f"🎯 is_playing is now: {self.is_playing}")
        
        # Process any pending UI events
        self.root.update()
        print(f"🎯 After root.update(), is_playing: {self.is_playing}")
        
        # Run generation directly (no threading)
        self._generate_meditation_direct(meditation_text)
    
    def _generate_meditation_direct(self, meditation_text):
        """Generate meditation directly (no threading)"""
        try:
            print(f"🎯 Starting meditation generation, is_playing: {self.is_playing}")
            
            # Create output directory if it doesn't exist
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            print(f"📁 Output directory ready: {output_dir}")
            
            # Parse meditation text
            segments = self.parse_meditation_text(meditation_text)
            
            # Estimate total meditation duration
            estimated_duration = self.estimate_meditation_duration(segments)
            
            # Update status
            self.status_label.config(text="Creating audio segments...")
            
            # Generate audio for each text segment
            audio_files = []
            text_segments = [seg for seg in segments if seg[0] == 'text']
            text_segment_count = len(text_segments)
            current_text_segment = 0
            
            for i, (segment_type, content) in enumerate(segments):
                if not self.is_playing:  # Check if stopped
                    print(f"🛑 Generation stopped by user, is_playing: {self.is_playing}")
                    return
                
                if segment_type == 'text':
                    current_text_segment += 1
                    # Update progress status
                    progress_msg = f"Creating audio segment {current_text_segment}/{text_segment_count}..."
                    self.status_label.config(text=progress_msg)
                    self.root.update()  # Force UI update
                    
                    print(f"\n[TEXT] Processing segment {current_text_segment}/{text_segment_count}")
                    print(f"Text: {content[:60]}...")
                    
                    # Create audio file in current directory
                    audio_filename = f"output/meditation_segment_{current_text_segment:02d}.wav"
                    
                    try:
                        self.text_to_speech_file(content, audio_filename)
                        
                        # Verify the file was created successfully
                        if os.path.exists(audio_filename) and os.path.getsize(audio_filename) > 0:
                            print(f"✅ Segment {current_text_segment} completed successfully")
                            print(f"📁 Saved as: {audio_filename}")
                            audio_files.append(('audio', audio_filename))
                            self.generated_audio_files.append(audio_filename)
                        else:
                            print(f"❌ Segment {current_text_segment} failed - file not created")
                            # Still add it to the list so the meditation continues
                            audio_files.append(('audio', audio_filename))
                            self.generated_audio_files.append(audio_filename)
                            
                    except Exception as e:
                        print(f"❌ Error processing segment {current_text_segment}: {e}")
                        # Create silent audio as fallback
                        self._create_silent_audio(audio_filename, duration=len(content.split()) * 0.5)
                        audio_files.append(('audio', audio_filename))
                        self.generated_audio_files.append(audio_filename)
                        
                elif segment_type == 'pause':
                    print(f"⏸ Adding {content} second pause")
                    audio_files.append(('pause', content))
            
            # Skip playback and go directly to creating final file
            self.status_label.config(text="Creating final meditation file...")
            self.progress.stop()
            self.root.update()
            
            if self.is_playing:
                file_count = len([f for f in self.generated_audio_files if os.path.exists(f)])
                
                try:
                    final_filename = self.create_final_meditation_file(audio_files, estimated_duration)
                    if final_filename:
                        # Clean up individual segment files after successful final file creation
                        self.cleanup_segment_files()
                        self.status_label.config(text=f"Final meditation file created! 🎵 {final_filename}")
                        print(f"🎉 Meditation generation complete! Final file: {final_filename}")
                        print(f"🧹 Individual segments cleaned up - only final file remains")
                    else:
                        self.status_label.config(text=f"Meditation segments created! 🧘 ({file_count} files)")
                        print(f"🎉 {file_count} meditation segments created successfully!")
                except Exception as e:
                    print(f"❌ Failed to create final file: {e}")
                    self.status_label.config(text=f"Meditation segments created! 🧘 ({file_count} files)")
                    print("💾 Individual segments kept since final file creation failed")
                
                # Stop without playing
                self.stop_meditation()
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.stop_meditation()
    
    def stop_meditation(self):
        """Stop meditation playback"""
        print("🛑 stop_meditation() called")
        self.is_playing = False
        self.is_paused = False
        
        # Stop all audio
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        
        # Reset UI
        self.generate_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.progress.stop()
        self.status_label.config(text="Ready to create your meditation file")
        
        # Clear the audio files list (files may have been cleaned up)
        remaining_files = [f for f in self.generated_audio_files if os.path.exists(f)]
        if remaining_files:
            print(f"💾 Remaining audio files in current directory:")
            for audio_file in remaining_files:
                print(f"  📁 {audio_file}")
        
        self.generated_audio_files.clear()
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.stop_meditation()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    
    # Set icon (if available)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    app = MeditationGenerator(root)
    
    # Handle window close
    def on_closing():
        app.stop_meditation()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()
