"""
Conversation memory management for BhashaVox AI
"""

class ConversationMemory:
    def __init__(self, max_history=10):
        """
        Initialize conversation memory
        
        Args:
            max_history: Maximum number of conversation turns to remember
        """
        self.max_history = max_history
        self.history = []
        self.user_level = None
        self.session_start = None
    
    def add_message(self, role, message):
        """
        Add a message to conversation history
        
        Args:
            role: 'user' or 'assistant'
            message: The message content
        """
        self.history.append({
            "role": role,
            "message": message
        })
        
        # Keep only recent history
        if len(self.history) > self.max_history * 2:  # *2 because each turn has 2 messages
            self.history = self.history[-self.max_history * 2:]
    
    def get_history_string(self):
        """
        Get conversation history as a formatted string
        
        Returns:
            Formatted conversation history
        """
        if not self.history:
            return ""
        
        history_str = ""
        for msg in self.history:
            role_name = "User" if msg["role"] == "user" else "BhashaVox AI"
            history_str += f"{role_name}: {msg['message']}\n"
        
        return history_str
    
    def get_recent_messages(self, n=5):
        """
        Get the last N messages
        
        Args:
            n: Number of recent messages to retrieve
            
        Returns:
            List of recent messages
        """
        return self.history[-n:] if self.history else []
    
    def set_user_level(self, level):
        """
        Set user's proficiency level
        
        Args:
            level: Beginner, Intermediate, or Advanced
        """
        self.user_level = level
    
    def get_user_level(self):
        """
        Get user's proficiency level
        
        Returns:
            User level or None if not set
        """
        return self.user_level
    
    def clear_history(self):
        """
        Clear conversation history
        """
        self.history = []
    
    def get_conversation_count(self):
        """
        Get number of conversation turns
        
        Returns:
            Number of turns (user messages)
        """
        return len([msg for msg in self.history if msg["role"] == "user"])