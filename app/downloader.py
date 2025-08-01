import yt_dlp
import os 

DOWNLOAD_PATH = os.path.join(os.getcwd(), "downloads")


def get_mp3(url:str) -> str: 
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", '.mp3').replace('.m4a', '.mp3')
        return filename