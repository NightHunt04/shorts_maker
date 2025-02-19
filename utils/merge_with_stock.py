from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, CompositeVideoClip, CompositeAudioClip, vfx
import string, os

def normalize_word(word):
    return word.strip().lower().strip(string.punctuation)

def merge_short(
        idx, 
        input_video, 
        video_uuid, 
        output_video, 
        words, 
        segments, 
        THREADS_TO_BE_USED, 
        media = 'image', 
        background_music = None, 
        background_music_volume = 0.4
    ):
    video = VideoFileClip(input_video)
    b_roll_data = []
    words = [normalize_word(word) for word in words]
    counter = 0

    if media == 'image':
        for segment in segments['segments']:
            for word_info in segment['words']:
                word = normalize_word(word_info['word'])
                print(word, ':', words)
                if word in words:
                    if os.path.exists(f'media/stock_media/{video_uuid}/{idx}/{counter}.jpg'):
                        b_roll_data.append((f'media/stock_media/{video_uuid}/{idx}/{counter}.jpg', word_info['start']))
                        words.remove(word)
                        counter += 1

    b_roll_clips = []
    audio_effects_clips = []

    for b_roll_path, start_time in b_roll_data:
        b_roll_clip = ( 
            ImageClip(b_roll_path)
            .set_duration(2)
            .fx(vfx.resize, width=video.w, height=video.h)
            .set_position('center')
            .set_start(start_time)
            .fx(vfx.fadein, 0.5)
            .fx(vfx.fadeout, 0.5)
        )
        b_roll_clips.append(b_roll_clip)
        audio_effect_clip = AudioFileClip('sound_effects/click1.mp3').set_start(start_time)
        audio_effects_clips.append(audio_effect_clip)

    final_clip = CompositeVideoClip([video] + b_roll_clips)

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

    bgm_audio = None
    if background_music:
        if int(background_music) >= 0 and int(background_music) < len(bgm):
            bgm_music = bgm[int(background_music)]
            bgm_audio = AudioFileClip(bgm_music).set_duration(video.duration).volumex(background_music_volume)

    if video.audio is not None:
        if bgm_audio:
            final_audio = CompositeAudioClip([bgm_audio, video.audio] + audio_effects_clips)
        else:
            final_audio = CompositeAudioClip([video.audio] + audio_effects_clips)
    else:
        final_audio = CompositeAudioClip(audio_effects_clips)

    final_clip = final_clip.set_audio(final_audio)

    final_clip.write_videofile(
        output_video, 
        codec = 'libx264', 
        audio_codec = 'aac',
        preset = 'ultrafast',
        threads = THREADS_TO_BE_USED,
        fps = video.fps
    )
    video.close()
    for clip in b_roll_clips:
        clip.close()
    for audio in audio_effects_clips:
        audio.close()
    final_clip.close()

