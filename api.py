import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pipeline import run_pipeline
from config import OUTPUT_DIR

app = FastAPI(title="DublaJá API", version="1.0.0")

class DubRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return {"service": "DublaJá", "status": "online", "usage": "POST /dub"}

@app.post("/dub")
def dub_video(request: DubRequest):
    url = request.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL obrigatória")
    if 'youtube.com' not in url and 'youtu.be' not in url:
        raise HTTPException(status_code=400, detail="URL deve ser do YouTube")
    try:
        result = run_pipeline(url)
        return {
            "status": "success",
            "title": result['title'],
            "download_url": f"/download/{result['output_filename']}",
            "file_size_mb": result['file_size_mb'],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return FileResponse(path=file_path, filename=filename, media_type="video/mp4")
