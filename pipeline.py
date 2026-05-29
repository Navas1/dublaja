import os
import subprocess
from config import WORK_DIR, OUTPUT_DIR
from downloader import download_video
from transcriber import transcribe
from translator import translate_segments
from synthesizer import synthesize_speech, concatenate_audio_segments

def run_pipeline(youtube_url):
    print("\n" + "="*50)
    print("🎬 DUBLAJÁ - Pipeline de Dublagem")
    print("="*50)
    print("\n📌 ETAPA 1/5 - Baixando vídeo...")
    video_info = download_video(youtube_url)
    video_path = video_info['video_path']
    print("\n📌 ETAPA 2/5 - Extraindo áudio...")
    audio_original = os.path.join(WORK_DIR, "audio_original.wav")
    subprocess.run(['ffmpeg','-i',video_path,'-vn','-acodec','pcm_s16le','-ar','16000','-ac','1',audio_original,'-y'], capture_output=True)
    if not os.path.exists(audio_original):
        raise Exception("Falha ao extrair áudio")
    print("\n📌 ETAPA 3/5 - Transcrevendo áudio (Groq)...")
    transcription = transcribe(audio_original)
    if not transcription['segments']:
        raise Exception("Nenhuma fala detectada")
    print("\n📌 ETAPA 4/5 - Traduzindo para português...")
    translated = translate_segments(transcription['segments'])
    print("\n📌 ETAPA 5/5 - Gerando dublagem (TTS)...")
    tts_segments = synthesize_speech(translated)
    if not tts_segments:
        raise Exception("Falha ao gerar áudio dublado")
    dubbed_audio = concatenate_audio_segments(tts_segments)
    print("\n🎬 Montando vídeo final...")
    output_filename = f"dublaja_{video_info['video_id']}.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    subprocess.run(['ffmpeg','-i',video_path,'-i',dubbed_audio,'-c:v','copy','-map','0:v:0','-map','1:a:0',output_path,'-y'], capture_output=True)
    if not os.path.exists(output_path):
        raise Exception("Falha ao gerar vídeo final")
    file_size_mb = os.path.getsize(output_path) / (1024*1024)
    print("\n" + "="*50)
    print("✅ DUBLAJÁ - Concluído!")
    print(f"📁 Arquivo: {output_path}")
    print(f"📊 Tamanho: {file_size_mb:.1f} MB")
    print("="*50)
    return {'output_path':output_path,'output_filename':output_filename,'title':video_info['title'],'duration':video_info['duration'],'file_size_mb':round(file_size_mb,2)}
