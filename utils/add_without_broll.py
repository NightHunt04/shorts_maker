from moviepy.editor import AudioFileClip, CompositeAudioClip, VideoFileClip
from utils.transcribe_whisper import transcribe_whisper
from utils.add_subtitles import add_subtitles
import os

def add_without_broll(
        video_uuid, 
        THREADS_TO_BE_USED, 
        words_per_subtitle = 3, 
        kinetic_subtitles = False,
        font_size = 19,
        font_color = 'white',
        background_color = 'transparent-0',
        font_highlight_color = 'yellow-1',
        italic = False,
        bold = False,
        font_highlight_size = 24,
        subtitles_position = 'center',
        font_family = 'Tahoma',
        background_music = None,
        background_music_volume = 0.4
    ):
    if not os.path.exists(f'media/final_clips'):
        os.mkdir(f'media/final_clips')
    if not os.path.exists(f'media/final_clips/{video_uuid}'):
        os.mkdir(f'media/final_clips/{video_uuid}')

    try:
        for ind in range(len(os.listdir(f'media/cropped_clips/{video_uuid}'))):
            audio_path = f"media/audio_files/{video_uuid}/{ind}.mp3"
            segments = transcribe_whisper(audio_path)[0]
            
            bgm = [
                'music/Into-timelapse.mp3',
                'music/Echo-Sax-End.mp3',
                'music/piano-0.mp3',
                'music/piano-1.mp3',
                'music/adventure-intro.mp3',
                'music/uplifting-fairy-tale.mp3',
                'music/soul-voyager-epic-cinematic.mp3',
                'music/astroscape-motivation.mp3',
                'music/adventure-music-prime-facts.mp3',
            ]
            if int(background_music) >= 0 and int(background_music) < len(bgm):
                bgm = bgm[int(background_music)]
                add_subtitles(
                    segments = segments, 
                    input_video = f"media/cropped_clips/{video_uuid}/{ind}.mp4", 
                    output_path = f"media/final_clips/{video_uuid}/{ind}_without_bgm.mp4", 
                    video_uuid = video_uuid, 
                    words_per_subtitle = words_per_subtitle, 
                    kinetic_subtitles = kinetic_subtitles,
                    font_size = font_size,
                    font_color = font_color,
                    background_color = background_color,
                    font_highlight_color = font_highlight_color,
                    italic = italic,
                    bold = bold,
                    font_highlight_size = font_highlight_size,
                    subtitles_position = subtitles_position,
                    font_family = font_family,
                )
                video = VideoFileClip(f"media/final_clips/{video_uuid}/{ind}_without_bgm.mp4")
                music = AudioFileClip(bgm).set_duration(video.duration).volumex(background_music_volume)
                combined_audio = CompositeAudioClip([video.audio, music])
                video = video.set_audio(combined_audio)
                video.write_videofile(
                    f"media/final_clips/{video_uuid}/{ind}.mp4", 
                    codec = "libx264",
                    audio_codec = "aac",
                    threads = THREADS_TO_BE_USED
                )
                print(f'✅ - made clip {ind} without b-roll successfully')
            else:
                add_subtitles(
                    segments = segments, 
                    input_video = f"media/cropped_clips/{video_uuid}/{ind}.mp4", 
                    output_path = f"media/final_clips/{video_uuid}/{ind}.mp4", 
                    video_uuid = video_uuid, 
                    words_per_subtitle = words_per_subtitle, 
                    kinetic_subtitles = kinetic_subtitles,
                    font_size = font_size,
                    font_color = font_color,
                    background_color = background_color,
                    font_highlight_color = font_highlight_color,
                    italic = italic,
                    bold = bold,
                    font_highlight_size = font_highlight_size,
                    subtitles_position = subtitles_position,
                    font_family = font_family,
                )
                print(f'✅ - made clip {ind} without b-roll successfully')
        return "✅ - all clips made without b-roll successfully"
    except Exception as e:
        return f"❗- Error adding without b-roll: {str(e)}"
