"""
FastAPI backend for BhashaVox AI with Voice Support
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ai_engine import BhashaVoxEngine
from typing import Optional
import io

# Try to import voice module (optional)
try:
    from voice_module import VoiceHandler
    VOICE_AVAILABLE = True
    voice_handler = VoiceHandler()
except ImportError:
    VOICE_AVAILABLE = False
    voice_handler = None
    print("⚠️ Voice features not available. Install: pip install SpeechRecognition pyttsx3 pyaudio")

# Initialize FastAPI app
app = FastAPI(
    title="BhashaVox AI API",
    description="English Speaking Coach powered by Local LLM",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Engine
engine = BhashaVoxEngine()

# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    corrections_made: bool
    message_count: int

class StatusResponse(BaseModel):
    status: str
    message: str
    model: str

class StatsResponse(BaseModel):
    total_messages: int
    corrections_made: int
    accuracy_rate: float
    conversation_turns: int
    session_duration_minutes: float
    user_level: Optional[str]
    common_mistakes: dict

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": "BhashaVox AI",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/status", response_model=StatusResponse)
async def check_status():
    """Check if Ollama and model are available"""
    is_running, message = engine.check_ollama_status()
    
    return StatusResponse(
        status="online" if is_running else "offline",
        message=message,
        model=engine.model_name
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint
    
    Args:
        request: ChatRequest with user message
        
    Returns:
        ChatResponse with AI response
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Get AI response
        ai_response = engine.chat(request.message)
        
        # Check if corrections were made
        corrections_made = "✅" in ai_response or "Corrected:" in ai_response
        
        return ChatResponse(
            response=ai_response,
            corrections_made=corrections_made,
            message_count=engine.memory.get_conversation_count()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.post("/assess-level")
async def assess_level(request: ChatRequest):
    """
    Assess user's English proficiency level
    
    Args:
        request: ChatRequest with sample message
        
    Returns:
        Detected proficiency level
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        level = engine.assess_level(request.message)
        return {
            "level": level,
            "message": f"Your English level appears to be: {level}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assessing level: {str(e)}")

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get session statistics"""
    try:
        stats = engine.get_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

@app.post("/reset")
async def reset_session():
    """Reset conversation and analytics"""
    try:
        message = engine.reset_session()
        return {"message": message, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting session: {str(e)}")

@app.get("/history")
async def get_history():
    """Get conversation history"""
    try:
        history = engine.memory.history
        return {
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")

# Voice Endpoints

@app.get("/voice/status")
async def voice_status():
    """Check if voice features are available"""
    return {
        "voice_available": VOICE_AVAILABLE,
        "message": "Voice features enabled" if VOICE_AVAILABLE else "Voice features not available"
    }

@app.post("/voice/speech-to-text")
async def speech_to_text(audio_file: UploadFile = File(...)):
    """
    Convert speech audio to text
    
    Args:
        audio_file: Audio file (WAV format preferred)
        
    Returns:
        Recognized text
    """
    if not VOICE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Voice features not available")
    
    try:
        import speech_recognition as sr
        
        # Read audio file
        audio_data = await audio_file.read()
        
        # Convert to AudioData object
        recognizer = sr.Recognizer()
        
        # Save to temporary file and recognize
        with io.BytesIO(audio_data) as audio_buffer:
            with sr.AudioFile(audio_buffer) as source:
                audio = recognizer.record(source)
        
        # Recognize speech
        text = recognizer.recognize_google(audio, language='en-US')
        
        return {
            "text": text,
            "status": "success"
        }
    
    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="Could not understand audio")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Recognition error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/voice/text-to-speech")
async def text_to_speech(request: ChatRequest):
    """
    Convert text to speech audio
    
    Args:
        request: ChatRequest with text to convert
        
    Returns:
        Audio file stream
    """
    if not VOICE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Voice features not available")
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        import tempfile
        import os
        
        # Create temporary file for audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_path = temp_file.name
        temp_file.close()
        
        # Generate speech and save to file
        voice_handler.tts_engine.save_to_file(request.message, temp_path)
        voice_handler.tts_engine.runAndWait()
        
        # Read the file
        with open(temp_path, 'rb') as audio_file:
            audio_data = audio_file.read()
        
        # Clean up
        os.unlink(temp_path)
        
        # Return audio stream
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=speech.wav"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating speech: {str(e)}")

@app.post("/voice/chat")
async def voice_chat(request: ChatRequest):
    """
    Complete voice chat: takes text, returns AI response with audio
    
    Args:
        request: ChatRequest with user message
        
    Returns:
        Response text and audio URL
    """
    if not VOICE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Voice features not available")
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Get AI response
        ai_response = engine.chat(request.message)
        
        # Check if corrections were made
        corrections_made = "✅" in ai_response or "Corrected:" in ai_response
        
        return {
            "response": ai_response,
            "corrections_made": corrections_made,
            "message_count": engine.memory.get_conversation_count(),
            "audio_available": True,
            "note": "Use /voice/text-to-speech endpoint to get audio"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

# Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)