"""
Analytics and mistake tracking for BhashaVox AI
"""

from datetime import datetime
from collections import defaultdict

class AnalyticsTracker:
    def __init__(self):
        """
        Initialize analytics tracker
        """
        self.mistakes = []
        self.corrections_made = 0
        self.total_messages = 0
        self.mistake_categories = defaultdict(int)
        self.session_start = datetime.now()
    
    def log_mistake(self, original, corrected, category="grammar"):
        """
        Log a grammar/vocabulary mistake
        
        Args:
            original: Original incorrect text
            corrected: Corrected text
            category: Type of mistake (grammar, vocabulary, spelling, etc.)
        """
        self.mistakes.append({
            "timestamp": datetime.now(),
            "original": original,
            "corrected": corrected,
            "category": category
        })
        self.corrections_made += 1
        self.mistake_categories[category] += 1
    
    def log_message(self):
        """
        Increment total message count
        """
        self.total_messages += 1
    
    def get_accuracy_rate(self):
        """
        Calculate accuracy rate
        
        Returns:
            Percentage of messages without mistakes
        """
        if self.total_messages == 0:
            return 100.0
        
        messages_with_mistakes = len(self.mistakes)
        accuracy = ((self.total_messages - messages_with_mistakes) / self.total_messages) * 100
        return round(accuracy, 2)
    
    def get_common_mistakes(self, top_n=5):
        """
        Get most common mistake categories
        
        Args:
            top_n: Number of top categories to return
            
        Returns:
            List of (category, count) tuples
        """
        sorted_categories = sorted(
            self.mistake_categories.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_categories[:top_n]
    
    def get_session_summary(self):
        """
        Get summary of current session
        
        Returns:
            Dictionary with session statistics
        """
        session_duration = (datetime.now() - self.session_start).total_seconds() / 60
        
        return {
            "total_messages": self.total_messages,
            "corrections_made": self.corrections_made,
            "accuracy_rate": self.get_accuracy_rate(),
            "session_duration_minutes": round(session_duration, 2),
            "common_mistakes": dict(self.get_common_mistakes()),
            "total_mistake_types": len(self.mistake_categories)
        }
    
    def get_recent_mistakes(self, n=5):
        """
        Get recent mistakes
        
        Args:
            n: Number of recent mistakes to retrieve
            
        Returns:
            List of recent mistakes
        """
        return self.mistakes[-n:] if self.mistakes else []
    
    def reset_session(self):
        """
        Reset session statistics
        """
        self.mistakes = []
        self.corrections_made = 0
        self.total_messages = 0
        self.mistake_categories = defaultdict(int)
        self.session_start = datetime.now()