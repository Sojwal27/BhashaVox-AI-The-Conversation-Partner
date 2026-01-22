"""
Voice-enabled chat interface for BhashaVox AI
"""

from ai_engine import BhashaVoxEngine
from voice_module import VoiceHandler
import sys

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("🗣️  BhashaVox AI - Voice Mode")
    print("="*60)
    print("Commands:")
    print("  • Press ENTER to speak (voice input)")
    print("  • Type 'text' to switch to text mode")
    print("  • Type 'stats' to view statistics")
    print("  • Type 'test' to test microphone and speakers")
    print("  • Type 'speed [100-200]' to adjust voice speed")
    print("  • Type 'quit' or 'exit' to exit")
    print("="*60 + "\n")

def print_stats(stats):
    """Print session statistics"""
    print("\n" + "="*60)
    print("📊 SESSION STATISTICS")
    print("="*60)
    print(f"Total Messages: {stats['total_messages']}")
    print(f"Corrections Made: {stats['corrections_made']}")
    print(f"Accuracy Rate: {stats['accuracy_rate']}%")
    print(f"Conversation Turns: {stats['conversation_turns']}")
    print(f"Session Duration: {stats['session_duration_minutes']} minutes")
    
    if stats.get('user_level'):
        print(f"User Level: {stats['user_level']}")
    
    if stats['common_mistakes']:
        print("\nCommon Mistake Types:")
        for mistake_type, count in stats['common_mistakes'].items():
            print(f"  • {mistake_type}: {count}")
    
    print("="*60 + "\n")

def main():
    """Main voice chat loop"""
    print_banner()
    
    # Initialize engine
    print("🔧 Initializing AI Engine...")
    engine = BhashaVoxEngine()
    
    # Check Ollama status
    is_running, status_msg = engine.check_ollama_status()
    print(status_msg)
    
    if not is_running:
        print("\n⚠️ Please fix the above issue before continuing.\n")
        sys.exit(1)
    
    # Initialize voice handler
    print("\n🔧 Initializing Voice Module...")
    try:
        voice = VoiceHandler()
        voice_mode = True
        print("✅ Voice mode ready!\n")
    except Exception as e:
        print(f"❌ Voice initialization failed: {e}")
        print("💡 Falling back to text mode\n")
        voice = None
        voice_mode = False
    
    print("✨ Ready to chat! Press ENTER to speak or type your message...\n")
    
    # Main loop
    while True:
        try:
            # Get user input
            if voice_mode:
                user_input = input("Press ENTER to speak (or type command): ").strip()
                
                # If user pressed ENTER without typing, use voice input
                if not user_input:
                    user_text = voice.listen()
                    
                    if user_text:
                        print(f"\n🎤 You said: {user_text}\n")
                        user_input = user_text
                    else:
                        print("❌ No speech detected. Try again.\n")
                        continue
            else:
                user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit']:
                if voice and voice_mode:
                    voice.speak("Goodbye! Keep practicing your English!")
                print("\n👋 Thanks for practicing! Keep improving your English!\n")
                break
            
            elif user_input.lower() == 'stats':
                stats = engine.get_stats()
                print_stats(stats)
                continue
            
            elif user_input.lower() == 'reset':
                result = engine.reset_session()
                print(f"\n✅ {result}\n")
                if voice and voice_mode:
                    voice.speak(result)
                continue
            
            elif user_input.lower() == 'text':
                voice_mode = False
                print("\n📝 Switched to text mode\n")
                continue
            
            elif user_input.lower() == 'voice':
                if voice:
                    voice_mode = True
                    print("\n🎤 Switched to voice mode\n")
                else:
                    print("\n⚠️ Voice module not available\n")
                continue
            
            elif user_input.lower() == 'test':
                if voice:
                    voice.test_microphone()
                    voice.test_speakers()
                else:
                    print("⚠️ Voice module not available\n")
                continue
            
            elif user_input.lower().startswith('speed '):
                try:
                    speed = int(user_input.split()[1])
                    if 100 <= speed <= 200:
                        voice.set_voice_speed(speed)
                        print(f"✅ Voice speed set to {speed} WPM\n")
                    else:
                        print("⚠️ Speed must be between 100 and 200\n")
                except:
                    print("⚠️ Usage: speed [100-200]\n")
                continue
            
            # Get AI response
            print("\n🤖 BhashaVox AI: ", end="", flush=True)
            response = engine.chat(user_input)
            print(response)
            
            # Speak the response if in voice mode
            if voice and voice_mode:
                print("\n🔊 Speaking response...")
                voice.speak(response, wait=True)
            
            print()  # Empty line for readability
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()