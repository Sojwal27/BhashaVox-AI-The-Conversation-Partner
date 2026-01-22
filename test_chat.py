"""
CLI testing interface for BhashaVox AI
"""

from ai_engine import BhashaVoxEngine
import sys

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("🗣️  BhashaVox AI - English Speaking Coach")
    print("="*60)
    print("Commands:")
    print("  • Type your message to chat")
    print("  • 'stats' - View session statistics")
    print("  • 'reset' - Reset conversation")
    print("  • 'quit' or 'exit' - Exit the program")
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
    """Main CLI loop"""
    print_banner()
    
    # Initialize engine
    engine = BhashaVoxEngine()
    
    # Check Ollama status
    is_running, status_msg = engine.check_ollama_status()
    print(status_msg)
    
    if not is_running:
        print("\n⚠️ Please fix the above issue before continuing.\n")
        sys.exit(1)
    
    print("\n✨ Ready to chat! Start the conversation...\n")
    
    # Main loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit']:
                print("\n👋 Thanks for practicing! Keep improving your English!\n")
                break
            
            elif user_input.lower() == 'stats':
                stats = engine.get_stats()
                print_stats(stats)
                continue
            
            elif user_input.lower() == 'reset':
                result = engine.reset_session()
                print(f"\n✅ {result}\n")
                continue
            
            # Get AI response
            print("\nBhashaVox AI: ", end="", flush=True)
            response = engine.chat(user_input)
            print(response + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()