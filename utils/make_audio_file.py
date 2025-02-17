from moviepy.editor import VideoFileClip
import os

def make_audio_file(video_uuid):
    if not os.path.exists('media/audio_files/'):
        os.mkdir('media/audio_files/')
    if not os.path.exists(f'media/audio_files/{video_uuid}'):
        os.mkdir(f'media/audio_files/{video_uuid}')
        
    try:
        for ind in range(len(os.listdir(f'media/cropped_clips/{video_uuid}'))):
            clip = VideoFileClip(f"media/cropped_clips/{video_uuid}/{ind}.mp4")
            clip.audio.write_audiofile(f"media/audio_files/{video_uuid}/{ind}.mp3")
            print(f'✅ - audio file {ind}.mp3 created successfully')
        return "✅ - audio files created successfully"
    except Exception as e:
        return f"❗- Error making audio files: {str(e)}"

def make_single_audio_file(video, video_uuid):
    try:
        video = VideoFileClip(video)
        video.audio.write_audiofile(f"media/audio_files/{video_uuid}.mp3")
        return f'✅ - audio file {video_uuid}.mp3 created successfully'
    except Exception as e:
        return f"❗- Error making audio files: {str(e)}"