import os
from groq import Groq
from config import GROQ_API_KEY, WHISPER_MODEL

def transcribe(audio_path: str) -> dict:
    """Transcreve áudio usando Groq Whisper API (rápido e preciso)."""
    print(f"🎙️ Transcrevendo áudio via Groq: {audio_path}")

    client = Groq(api_key=GROQ_API_KEY)

    file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    print(f"📊 Tamanho do áudio: {file_size_mb:.1f} MB")

    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            file=audio_file,
            model=WHISPER_MODEL,
            language="en",
            response_format="verbose_json",
        )

    segments = []
    if hasattr(result, 'segments') and result.segments:
        for seg in result.segments:
            segments.append({
                'start': round(seg['start'], 2),
                'end': round(seg['end'], 2),
                'text': seg['text'].strip(),
            })
    else:
        segments.append({
            'start': 0,
            'end': 0,
            'text': result.text.strip(),
        })

    full_text = result.text.strip()
    print(f"✅ Transcrição concluída: {len(segments)} segmentos")
    print(f"📝 Preview: {full_text[:150]}...")

    return {
        'text': full_text,
        'segments': segments,
        'language': result.language if hasattr(result, 'language') else 'en',
    }
