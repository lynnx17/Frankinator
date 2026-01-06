from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import yt_dlp as ytdlp
import os
import sys

app = FastAPI()

# Bepaal base path zodat PyInstaller de juiste folders kan vinden
if getattr(sys, "frozen", False):
    # Als PyInstaller bundelt, zitten bestanden in _MEIPASS
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).parent

# Mount static en templates
app.mount("/static", StaticFiles(directory=base_path / "static"), name="static")
templates_dir = base_path / "templates"

tmp_dir = Path("/tmp")  # tijdelijke map voor downloads

@app.get("/", response_class=HTMLResponse)
async def index():
    index_file = templates_dir / "index.html"
    return HTMLResponse(index_file.read_text())

@app.post("/download")
async def download(url: str = Form(...), filename: str = Form(None)):
    try:
        with ytdlp.YoutubeDL({
            "format": "bestaudio/best",
            "outtmpl": str(tmp_dir / "%(title)s.%(ext)s"),
            "quiet": True,
            "noplaylist": True,
        }) as ydl:
            info = ydl.extract_info(url, download=True)

        base_name = filename.strip() if filename else info.get("title")
        mp3_file = tmp_dir / f"{base_name}.mp3"

        # Convert to mp3 using ffmpeg
        original_file = tmp_dir / f"{info.get('title')}.{info.get('ext')}"
        os.system(f'ffmpeg -y -i "{original_file}" "{mp3_file}"')
        os.remove(original_file)

        return FileResponse(mp3_file, filename=f"{mp3_file.name}", media_type="audio/mpeg")
    except Exception as e:
        return HTMLResponse(f"<h2>Error: {e}</h2>", status_code=500)
