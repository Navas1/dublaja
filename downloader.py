import os
import subprocess
from config import WORK_DIR, MAX_VIDEO_DURATION


def download_video(url: str) -> dict:
    """Baixa vídeo do YouTube e retorna caminhos + info."""
    print(f"📥 Baixando vídeo: {url}")

    info_cmd = [
        'yt-dlp', '--no-download', '--print', 'id',
        '--print', 'title', '--print', 'duration',
        url
    ]
    result = subprocess.run(info_cmd, capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')

    if len(lines) < 3:
        raise Exception("Não conseguiu ler informações do vídeo")

    video_id = lines[0].strip()
    title = lines[1].strip()
    duration = int(lines[2].strip())

    if duration > MAX_VIDEO_DURATION:
        raise ValueError(f"Vídeo muito longo ({duration}s). Máximo: {MAX_VIDEO_DURATION}s")

    output_path = os.path.join(WORK_DIR, f"{video_id}.mp4")

    print(f"🎬 Título: {title}")
    print(f"⏱️ Duração: {duration}s")
    print("🔄 Baixando...")

    subprocess.run([
        'yt-dlp',
        '-f', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '--merge-output-format', 'mp4',
        '-o', output_path,
        url
    ], check=True)

    if not os.path.exists(output_path):
        raise FileNotFoundError("Arquivo de vídeo não encontrado após download")

    print(f"✅ Vídeo baixado: {output_path}")

    return {
        'video_id': video_id,
        'video_path': output_path,
        'title': title,
        'duration': duration,
    }
