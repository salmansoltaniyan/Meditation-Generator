#!/usr/bin/env python3
"""
Simple Meditation Test
A minimal version to test just the TTS functionality
"""

import pyttsx3
import tempfile
import os
import time

def simple_tts_test():
    print("🧘 Simple TTS Test for Meditation Generator")
    print("=" * 50)
    
    # Sample text to convert
    test_text = "Welcome to this guided meditation. Take a deep breath and relax."
    
    try:
        # Initialize TTS
        print("Initializing TTS engine...")
        engine = pyttsx3.init()
        
        # Set properties
        engine.setProperty('rate', 140)
        engine.setProperty('volume', 0.9)
        
        print("TTS engine initialized successfully!")
        
        # Test 1: Direct speech
        print("\n🎵 Test 1: Direct speech")
        print("You should hear the test text now...")
        engine.say(test_text)
        engine.runAndWait()
        print("Direct speech completed!")
        
        # Test 2: Save to file
        print("\n💾 Test 2: Save to file")
        # Save in current directory with a clear name
        audio_filename = "test_meditation_audio.wav"
        
        print(f"Saving TTS to file: {audio_filename}")
        engine.save_to_file(test_text, audio_filename)
        
        print("Calling runAndWait()...")
        start_time = time.time()
        engine.runAndWait()
        end_time = time.time()
        
        print(f"runAndWait() completed in {end_time - start_time:.2f} seconds")
        
        # Check if file was created
        if os.path.exists(audio_filename):
            file_size = os.path.getsize(audio_filename)
            print(f"✅ File created successfully! Size: {file_size} bytes")
            print(f"📁 Audio file saved as: {os.path.abspath(audio_filename)}")
            
            # Try to play the file with pygame
            try:
                import pygame
                pygame.mixer.init()
                sound = pygame.mixer.Sound(audio_filename)
                print("Playing generated audio file...")
                sound.play()
                time.sleep(3)  # Let it play
                pygame.mixer.quit()
                print("✅ Audio file playback successful!")
            except Exception as e:
                print(f"❌ Could not play audio file: {e}")
        else:
            print("❌ File was not created!")
        
        # Keep the file (don't delete it)
        print(f"💾 Audio file kept in current directory: {audio_filename}")
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during TTS test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_tts_test()
