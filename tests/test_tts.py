#!/usr/bin/env python3
"""
TTS Diagnostic Script
Run this to test if text-to-speech is working on your system
"""

def test_tts():
    print("🔍 Testing Text-to-Speech functionality...")
    print("=" * 50)
    
    # Test 1: Import pyttsx3
    try:
        import pyttsx3
        print("✅ pyttsx3 imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import pyttsx3: {e}")
        print("💡 Solution: pip install pyttsx3")
        return False
    
    # Test 2: Initialize TTS engine
    try:
        engine = pyttsx3.init()
        print("✅ TTS engine initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize TTS engine: {e}")
        print("💡 Solution: Check if your system has TTS capabilities")
        return False
    
    # Test 3: Get available voices
    try:
        voices = engine.getProperty('voices')
        print(f"✅ Found {len(voices)} voice(s) available:")
        for i, voice in enumerate(voices[:3]):  # Show first 3 voices
            print(f"   {i+1}. {voice.name} (ID: {voice.id})")
        if len(voices) > 3:
            print(f"   ... and {len(voices)-3} more")
    except Exception as e:
        print(f"❌ Failed to get voices: {e}")
    
    # Test 4: Test speech properties
    try:
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        print(f"✅ Current settings - Rate: {rate}, Volume: {volume}")
    except Exception as e:
        print(f"❌ Failed to get speech properties: {e}")
    
    # Test 5: Test simple speech
    print("\n🎵 Testing simple speech...")
    try:
        engine.say("Hello, this is a test of text to speech.")
        engine.runAndWait()
        print("✅ Simple speech test completed")
    except Exception as e:
        print(f"❌ Simple speech test failed: {e}")
    
    # Test 6: Test file generation
    print("\n💾 Testing file generation...")
    try:
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        engine.save_to_file("This is a test for file generation.", temp_filename)
        engine.runAndWait()
        
        if os.path.exists(temp_filename) and os.path.getsize(temp_filename) > 0:
            print("✅ File generation test completed successfully")
            print(f"   Generated file: {temp_filename}")
            print(f"   File size: {os.path.getsize(temp_filename)} bytes")
        else:
            print("❌ File generation test failed - file is empty or doesn't exist")
        
        # Clean up
        try:
            os.unlink(temp_filename)
        except:
            pass
            
    except Exception as e:
        print(f"❌ File generation test failed: {e}")
    
    # Test 7: Test pygame audio
    print("\n🎮 Testing pygame audio...")
    try:
        import pygame
        pygame.mixer.init()
        print("✅ Pygame audio initialized successfully")
    except Exception as e:
        print(f"❌ Pygame audio test failed: {e}")
        print("💡 Solution: pip install pygame")
    
    print("\n" + "=" * 50)
    print("🎯 DIAGNOSIS COMPLETE")
    print("\nIf you see any ❌ errors above, those need to be fixed first.")
    print("If all tests pass ✅, the meditation app should work correctly.")
    
    return True

if __name__ == "__main__":
    test_tts()
    input("\nPress Enter to exit...")
