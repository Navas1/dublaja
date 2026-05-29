import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# === APIs ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# === Caminhos ===
WORK_DIR = os.getenv("WORK_DIR", "/tmp/dublaja")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/tmp/dublaja/output")

# === Tradução ===
TRANSLATOR_ENGINE = "google"

# === Voz TTS ===
TTS_VOICE = "pt-BR-FranciscoNeural"

# === Whisper ===
WHISPER_MODEL = "whisper-large-v3-turbo"

# === Limits ===
MAX_VIDEO_DURATION = 1200

os.makedirs(WORK_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
