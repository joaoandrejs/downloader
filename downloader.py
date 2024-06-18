import os
import re
from pytube import YouTube
from instaloader import Instaloader, Post
from moviepy.editor import VideoFileClip
import youtube_dl

def download_youtube_video(url, file_format):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=(file_format == 'mp3')).first() if file_format == 'mp3' else yt.streams.get_highest_resolution()
    file_path = stream.download()
    
    if file_format == 'mp3':
        convert_to_mp3(file_path)

    print(f"Download completo: {file_path}")

def download_instagram_video(url, file_format):
    loader = Instaloader(download_videos=True)
    shortcode = re.search(r"/p/([^/]+)/", url)
    if not shortcode:
        print("URL do Instagram inválida.")
        return
    
    post = Post.from_shortcode(loader.context, shortcode.group(1))
    file_path = loader.download_post(post, target='downloads')
    if file_format == 'mp3':
        video_file = next(file for file in os.listdir('downloads') if file.endswith('.mp4'))
        convert_to_mp3(os.path.join('downloads', video_file))
    print(f"Download completo: {file_path}")

def download_with_youtube_dl(url, file_format):
    ydl_opts = {
        'format': 'bestaudio/best' if file_format == 'mp3' else 'bestvideo+bestaudio',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}] if file_format == 'mp3' else [],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def convert_to_mp3(file_path):
    video_clip = VideoFileClip(file_path)
    audio_path = os.path.splitext(file_path)[0] + '.mp3'
    video_clip.audio.write_audiofile(audio_path)
    video_clip.close()
    os.remove(file_path)
    print(f"Convertido para mp3: {audio_path}")

def main():
    url = input("Envie a URL do vídeo: ")
    file_format = input("Selecione a opção de download:\n(1) MP3\n(2) MP4\n> ").replace('1', 'mp3').replace('2', 'mp4')
    print('\n> Baixando vídeo...')

    if file_format not in ['mp4', 'mp3']:
        print("Formato inválido. Por favor, selecione um dos formatos suportados: MP4 ou MP3.")
        return
    
    if 'youtube.com' in url or 'youtu.be' in url:
        download_youtube_video(url, file_format)
    elif 'instagram.com' in url:
        download_instagram_video(url, file_format)
    elif 'x.com' in url or 'twitter.com' in url or 'soundcloud.com' in url:
        download_with_youtube_dl(url, file_format)
    else:
        print("Site não suportado. Atualmente só suportamos os seguintes sites: YouTube, Instagram, Twitter, e SoundCloud.")

if __name__ == "__main__":
    main()
