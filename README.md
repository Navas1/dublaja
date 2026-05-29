# DublaJá

Dublagem automática de vídeos do YouTube — inglês para português.

## Como funciona

1. Usuário envia link
2. Vídeo baixado (yt-dlp)
3. Áudio transcrito (Groq Whisper)
4. Traduzido para português
5. Voz gerada (edge-tts)
6. Vídeo final montado

## Stack

- Python 3.12 + FastAPI
- Groq Whisper API
- deep-translator
- edge-tts + gTTS
- yt-dlp + ffmpeg

## Instalação

git clone https://github.com/Navas1/dublaja.git
cd dublaja
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

## Executar

python main.py

## Licença

MIT
