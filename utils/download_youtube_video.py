import yt_dlp

def download_youtube_video(url, user_uuid):
    try:
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[ext=mp4]', 
            'outtmpl': f'media/downloads/{user_uuid}.%(ext)s',
            'merge_output_format': 'mp4'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "✅ - video downloaded successfully"
    except Exception as e:
        return f"❗- Error downloading video: {str(e)}"