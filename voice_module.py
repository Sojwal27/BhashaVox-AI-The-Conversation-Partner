"""
Voice Module for BhashaVox AI
Handles Speech-to-Text and Text-to-Speech
"""

import speech_recognition as sr
import pyttsx3
import threading
from typing import Optional

class VoiceHandler:
    def __init__(self):
        """
        Initialize voice handler with STT and TTS
        """
        # Speech Recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Text to Speech
        self.tts_engine = pyttsx3.init()
        self._setup_tts()
        
        # Adjust for ambient noise on initialization
        print("🎤 Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Microphone ready!")
    
    def _setup_tts(self):
        """
        Configure Text-to-Speech settings
        """
        # Set properties
        self.tts_engine.setProperty('rate', 150)  # Speed (words per minute)
        self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Try to set a clear voice
        voices = self.tts_engine.getProperty('voices')
        
        # Prefer female voice for language learning (usually clearer)
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
    
    def listen(self, timeout=5, phrase_time_limit=10) -> Optional[str]:
        """
        Listen to microphone and convert speech to text
        
        Args:
            timeout: Seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for the phrase
            
        Returns:
            Recognized text or None if failed
        """
        try:
            with self.microphone as source:
                print("🎤 Listening... (speak now)")
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("🔄 Processing speech...")
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio, language='en-US')
                
                return text
                
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected (timeout)")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Could not request results; {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def speak(self, text: str, wait=True):
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
            wait: Whether to wait for speech to complete
        """
        try:
            # Remove emoji and special characters for cleaner speech
            clean_text = self._clean_text_for_speech(text)
            
            if wait:
                # Blocking call - waits until speech is complete
                self.tts_engine.say(clean_text)
                self.tts_engine.runAndWait()
            else:
                # Non-blocking call
                thread = threading.Thread(target=self._speak_async, args=(clean_text,))
                thread.daemon = True
                thread.start()
                
        except Exception as e:
            print(f"❌ TTS Error: {e}")
    
    def _speak_async(self, text: str):
        """
        Async speech method for non-blocking operation
        """
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def _clean_text_for_speech(self, text: str) -> str:
        """
        Clean text for better TTS pronunciation
        
        Args:
            text: Original text
            
        Returns:
            Cleaned text
        """
        # Remove common emojis and symbols
        emoji_dict = {
            '✅': 'Corrected: ',
            '💡': 'Tip: ',
            '💬': '',
            '🎯': '',
            '✨': '',
            '👋': '',
            '**': ''
        }
        
        for emoji, replacement in emoji_dict.items():
            text = text.replace(emoji, replacement)
        
        # Remove markdown formatting
        text = text.replace('**', '').replace('*', '')
        
        return text.strip()
    
    def set_voice_speed(self, rate: int):
        """
        Set speech rate
        
        Args:
            rate: Words per minute (typically 100-200)
        """
        self.tts_engine.setProperty('rate', rate)
    
    def set_voice_volume(self, volume: float):
        """
        Set speech volume
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.tts_engine.setProperty('volume', max(0.0, min(1.0, volume)))
    
    def list_available_voices(self):
        """
        List all available TTS voices
        
        Returns:
            List of voice information
        """
        voices = self.tts_engine.getProperty('voices')
        voice_list = []
        
        for idx, voice in enumerate(voices):
            voice_list.append({
                'id': idx,
                'name': voice.name,
                'languages': voice.languages,
                'gender': voice.gender if hasattr(voice, 'gender') else 'unknown'
            })
        
        return voice_list
    
    def test_microphone(self):
        """
        Test if microphone is working
        
        Returns:
            True if microphone is accessible
        """
        try:
            with self.microphone as source:
                print("🎤 Testing microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("✅ Microphone is working!")
                return True
        except Exception as e:
            print(f"❌ Microphone error: {e}")
            return False
    
    def test_speakers(self):
        """
        Test if speakers/TTS is working
        
        Returns:
            True if TTS is working
        """
        try:
            print("🔊 Testing speakers...")
            self.speak("Hello! I am BhashaVox AI. Can you hear me?", wait=True)
            print("✅ Speakers are working!")
            return True
        except Exception as e:
            print(f"❌ Speaker error: {e}")
            return False