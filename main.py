import yt_dlp
from pathlib import Path


def youtube_to_mp3(url: str, output_folder: str = ".") -> Path:
    """Download YouTube audio directly as MP3 using yt-dlp."""
    output_path = Path(output_folder).expanduser().resolve()
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = Path(ydl.prepare_filename(info)).with_suffix('.mp3')
            print(f"✅ Saved as: {filename}")
            return filename
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    url = input("Enter YouTube URL: ").strip()
    output_folder = input("Enter output folder (or press Enter for current): ").strip() or "."
    youtube_to_mp3(url, output_folder)
