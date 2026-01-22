"""
AI Engine for BhashaVox AI - Handles LLM interactions via Ollama
"""

import requests
import os
from dotenv import load_dotenv
from prompts import create_conversation_prompt, create_level_assessment_prompt
from memory import ConversationMemory
from analytics import AnalyticsTracker

load_dotenv()

class BhashaVoxEngine:
    def __init__(self):
        """
        Initialize the BhashaVox AI Engine
        """
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model_name = os.getenv("MODEL_NAME", "phi3:mini")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "500"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        
        self.memory = ConversationMemory()
        self.analytics = AnalyticsTracker()
        
    def call_ollama(self, prompt, temperature=None):
        """
        Call Ollama API with the given prompt
        
        Args:
            prompt: The prompt to send to the LLM
            temperature: Override default temperature
            
        Returns:
            LLM response text
        """
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature or self.temperature,
                        "num_predict": self.max_tokens
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"Error: Ollama returned status code {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure Ollama is running (ollama serve)"
        except requests.exceptions.Timeout:
            return "Error: Request timed out. The model might be loading."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def check_ollama_status(self):
        """
        Check if Ollama is running and model is available
        
        Returns:
            Tuple of (is_running, message)
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]
                
                if self.model_name in model_names:
                    return True, f"✅ Ollama is running with {self.model_name}"
                else:
                    return False, f"⚠️ Model {self.model_name} not found. Run: ollama pull {self.model_name}"
            else:
                return False, "⚠️ Ollama is running but returned an error"
        except:
            return False, "❌ Ollama is not running. Start it with: ollama serve"
    
    def chat(self, user_message):
        """
        Main chat function - processes user message and returns AI response
        
        Args:
            user_message: User's input message
            
        Returns:
            AI response
        """
        # Log message for analytics
        self.analytics.log_message()
        
        # Add user message to memory
        self.memory.add_message("user", user_message)
        
        # Get conversation history
        history = self.memory.get_history_string()
        
        # Create prompt with context
        prompt = create_conversation_prompt(user_message, history)
        
        # Get AI response
        ai_response = self.call_ollama(prompt)
        
        # Add AI response to memory
        self.memory.add_message("assistant", ai_response)
        
        # Detect if correction was made (simple heuristic)
        if "✅" in ai_response or "Corrected:" in ai_response:
            self.analytics.log_mistake(user_message, ai_response, "grammar")
        
        return ai_response
    
    def assess_level(self, user_message):
        """
        Assess user's English proficiency level
        
        Args:
            user_message: Sample message from user
            
        Returns:
            Proficiency level (Beginner/Intermediate/Advanced)
        """
        prompt = create_level_assessment_prompt(user_message)
        level = self.call_ollama(prompt, temperature=0.3).strip()
        
        # Validate and set level
        valid_levels = ["Beginner", "Intermediate", "Advanced"]
        for valid_level in valid_levels:
            if valid_level.lower() in level.lower():
                self.memory.set_user_level(valid_level)
                return valid_level
        
        return "Intermediate"  # Default
    
    def get_stats(self):
        """
        Get session statistics
        
        Returns:
            Dictionary with session stats
        """
        stats = self.analytics.get_session_summary()
        stats["conversation_turns"] = self.memory.get_conversation_count()
        stats["user_level"] = self.memory.get_user_level()
        return stats
    
    def reset_session(self):
        """
        Reset conversation and analytics
        """
        self.memory.clear_history()
        self.analytics.reset_session()
        return "Session reset successfully!"