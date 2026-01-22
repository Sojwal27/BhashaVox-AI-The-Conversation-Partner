# 🗣️ BhashaVox AI

**BhashaVox AI** is an LLM-powered English speaking conversation assistant designed to help users improve **fluency, grammar, vocabulary, and confidence** through natural conversations. It is optimized to run on **low-resource machines** using a **locally deployed LLM via Ollama**.

---

## ✨ Key Features

* 💬 Real-time English conversation practice
* ✍️ Automatic grammar correction with simple explanations
* 📈 Adaptive responses based on user proficiency level
* 🧠 Context-aware conversations using an LLM
* 💻 Runs locally (no cloud dependency)
* 🇮🇳 Indian-friendly learning approach

---

## 🧠 Core Technology

* **LLM Engine:** Phi-3 Mini (via Ollama)
* **Backend:** Python
* **LLM Interface:** Ollama REST API
* **Optional Extensions:** Speech-to-Text, Text-to-Speech

---

## 🏗️ System Architecture

```
┌────────────┐
│   User     │
│ (Text/Voice)│
└─────┬──────┘
      ↓
┌────────────┐
│  Input     │
│ Processing │
└─────┬──────┘
      ↓
┌──────────────────────┐
│  BhashaVox AI Engine │
│  (Prompt + Logic)   │
└─────┬────────────────┘
      ↓
┌──────────────────────┐
│ Local LLM (Phi-3 Mini)   │
│ via Ollama API      │
└─────┬────────────────┘
      ↓
┌────────────┐
│  Response  │
│ (Text/Voice)│
└────────────┘
```

---

## 📦 Project Structure

```
bhashavox-ai/
│
├── venv/                 # Virtual environment
├── ai_engine.py          # LLM + Ollama interaction
├── prompts.py            # Prompt definitions
├── memory.py             # Conversation memory
├── analytics.py          # Mistake tracking
├── main.py               # FastAPI backend
├── test_chat.py          # CLI testing
├── requirements.txt
├── .env
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

* Python 3.9+
* 4 GB RAM system
* Ollama installed

### 2️⃣ Install Ollama & LLM

```bash
ollama pull qwen2.5:0.5b
ollama run qwen2.5:0.5b
```

### 3️⃣ Install Python Dependencies

```bash
pip install requests python-dotenv fastapi uvicorn
```

---

## 🔌 LLM Integration (Gemma via Ollama)

```python
import requests

def bhashavox_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:0.5b",
            "prompt": prompt,
            "stream": False
        }
    )
        response.raise_for_status()  # HTTP error check
        return response.json().get("response", "")

    except requests.exceptions.RequestException as e:
        return f"Error connecting to LLM: {e}"
```

---

## 🧩 Prompt Design (Core Intelligence)

```text
You are BhashaVox AI, an English speaking coach.

Rules:
1. Correct grammar mistakes
2. Explain corrections simply
3. Encourage the user
4. Continue the conversation naturally
```

---

## 🧪 Example Interaction

**User:** I am go market yesterday

**BhashaVox AI:**

* **Correction:** I went to the market yesterday.
* **Explanation:** "Go" becomes "went" in the past tense.
* **Reply:** What did you buy at the market?

---

## 🧠 Model Choice Rationale

* **Qwen2.5 (0.5B)** is optimized for low-resource systems (≈4 GB RAM)
* Provides strong English understanding and grammar correction
* Fast inference on CPU-only machines
* Ideal for local, privacy-friendly AI applications

---

## 🔮 Future Enhancements

* 🎤 Voice-based conversation
* 📊 Fluency & grammar scoring
* 👤 User progress tracking
* 📱 Mobile app (Flutter)
* 🧠 Fine-tuned LLM for English learning

---

## 📌 Why BhashaVox AI?

* Works on low-end hardware
* Uses real LLM intelligence
* Privacy-friendly (local execution)
* Scalable from personal use to full product

---

## 🤝 Contribution

Contributions are welcome!

Steps:

1. Fork the repository
2. Create a new branch (`feature/your-feature`)
3. Commit changes
4. Open a Pull Request

---

## 📜 License

MIT License

---

> **BhashaVox AI** — Speak Better. Speak Confidently.
