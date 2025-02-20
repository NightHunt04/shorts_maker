from utils.image_generator import image_generator
from utils.search_words import search_words
from utils.transcribe_whisper import transcribe_whisper
from utils.add_subtitles import add_subtitles
from utils.merge_with_stock import merge_short
import os

def add_with_ai_broll(
        video_uuid, 
        THREADS_TO_BE_USED, 
        words_per_subtitle = 3,
        media = 'image', 
        kinetic_subtitles = False,
        font_size = 19,
        font_color = 'white',
        background_color = 'transparent-0',
        font_highlight_color = 'yellow',
        italic = False,
        bold = False,
        font_highlight_size = 24,
        subtitles_position = 'center',
        font_family = 'Tahoma',
        background_music = None,
        background_music_volume = 0.4,
        subtitles = None
    ):
    if not os.path.exists(f'media/final_clips'):
        os.mkdir(f'media/final_clips')
    if not os.path.exists(f'media/final_clips/{video_uuid}'):
        os.mkdir(f'media/final_clips/{video_uuid}')

    try:
        for ind in range(len(os.listdir(f'media/cropped_clips/{video_uuid}'))):
            audio_path = f"media/audio_files/{video_uuid}/{ind}.mp3"
            segments = transcribe_whisper(audio_path)[0]
            words = search_words(segments)
            image_generator(ind, words, video_uuid)
            merge_short(
                idx = ind, 
                input_video = f"media/cropped_clips/{video_uuid}/{ind}.mp4", 
                output_video = f"media/final_clips/{video_uuid}/{ind}_without_sub.mp4", 
                video_uuid = video_uuid, 
                words = words, 
                segments = segments, 
                media = media,
                THREADS_TO_BE_USED = THREADS_TO_BE_USED,
                background_music = background_music,
                background_music_volume = background_music_volume
            )
            if subtitles:
                add_subtitles(
                    segments = segments, 
                    input_video = f"media/final_clips/{video_uuid}/{ind}_without_sub.mp4", 
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
                    font_family = font_family
                )
            print(f'✅ - made clip {ind} with AI b-roll successfully')
        return "✅ - all clips made with AI b-roll successfully"
    except Exception as e:
        return f"❗- Error adding with AI b-roll: {str(e)}"