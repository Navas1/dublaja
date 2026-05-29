import os
import subprocess
from config import WORK_DIR

def _synth_edge_tts(text, audio_path):
    import asyncio, edge_tts
    async def _gen():
        c = edge_tts.Communicate(text, 'pt-BR-AntonioNeural')
        await c.save(audio_path)
    asyncio.run(_gen())

def _synth_gtts(text, audio_path):
    from gtts import gTTS
    tts = gTTS(text=text, lang='pt-br')
    tts.save(audio_path)

def synthesize_speech(segments, voice=None):
    audio_dir = os.path.join(WORK_DIR, "tts_segments")
    os.makedirs(audio_dir, exist_ok=True)
    full_text = " ".join(s.get('translated', s.get('text', '')) for s in segments if s.get('translated') or s.get('text'))
    print(f"🗣️ Texto completo: {len(full_text)} caracteres")
    full_audio_path = os.path.join(audio_dir, "full_text.mp3")
    try:
        _synth_edge_tts(full_text, full_audio_path)
        print("✅ edge-tts OK")
    except Exception:
        print("⚠️ edge-tts falhou, usando gTTS...")
        gtts_path = os.path.join(audio_dir, "full_text_gtts.mp3")
        _synth_gtts(full_text, gtts_path)
        os.rename(gtts_path, full_audio_path)
        print("✅ gTTS OK")
    if os.path.exists(full_audio_path) and os.path.getsize(full_audio_path) > 0:
        return [{'start': 0, 'end': 0, 'audio_path': full_audio_path, 'text': full_text}]
    raise Exception("Falha ao gerar áudio TTS")

def concatenate_audio_segments(audio_segments):
    from pydub import AudioSegment
    print("🔗 Processando áudio...")
    tts_path = audio_segments[0]['audio_path']
    tts_audio = AudioSegment.from_file(tts_path)
    tts_ms = len(tts_audio)
    tts_sec = tts_ms / 1000.0
    target = 19.0
    print(f"📊 TTS: {tts_sec:.1f}s | Alvo: {target:.1f}s")
    temp_in = os.path.join(WORK_DIR, "tts_raw.wav")
    temp_out = os.path.join(WORK_DIR, "tts_adjusted.wav")
    output_path = os.path.join(WORK_DIR, "dubbed_audio.wav")
    tts_audio.export(temp_in, format="wav")
    ratio = tts_sec / target
    atempo = max(0.5, min(2.0, ratio))
    print(f"🔄 Ajustando velocidade: {atempo:.2f}x")
    subprocess.run(['ffmpeg','-i',temp_in,'-filter:a',f'atempo={atempo:.4f}','-y',temp_out], capture_output=True)
    adjusted = AudioSegment.from_file(temp_out)
    adj_sec = len(adjusted) / 1000.0
    print(f"📊 Áudio ajustado: {adj_sec:.1f}s")
    target_ms = int(target * 1000)
    if len(adjusted) < target_ms:
        silence_needed = target_ms - len(adjusted)
        adjusted += AudioSegment.silent(duration=silence_needed)
        print(f"🔗 Silêncio final: {silence_needed/1000:.1f}s")
    adjusted.export(output_path, format="wav")
    final = AudioSegment.from_file(output_path)
    print(f"✅ Áudio final: {len(final)/1000:.1f}s")
    for f in [temp_in, temp_out]:
        if os.path.exists(f):
            os.remove(f)
    return output_path
