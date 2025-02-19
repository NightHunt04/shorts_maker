import os
from videoprops import get_video_properties
from moviepy.video.io.VideoFileClip import VideoFileClip

def trim_selected_clips(transcript, video_uuid, downloaded_video_path, threads, custom_timestamps = None, shorts_length = 60):
    try:
        # changed
        print(downloaded_video_path)
        video_props = get_video_properties(downloaded_video_path)
        target_resolution = (video_props['height'], video_props['width'])

        if custom_timestamps:
            segments = []
            separated_timestamps = custom_timestamps.split(';')
            for timestamp in separated_timestamps:
                if timestamp:
                    if timestamp.find('->') == -1:
                        start_time = float(timestamp.strip())
                        end_time = start_time + shorts_length
                    else:
                        start_time, end_time = timestamp.split('->')
                        start_time = float(start_time.strip())
                        end_time = float(end_time.strip())
                    segments.append({
                        'start': start_time,
                        'end': end_time
                    })
            
            for ind, segment in enumerate(segments):
                clip = VideoFileClip(
                    downloaded_video_path,  
                    audio = True, 
                    target_resolution = target_resolution
                )
                clip_fps = clip.fps
                trimmed_clip = clip.subclip(segment['start'], segment['end'])

                if not os.path.exists('media/trimmed_clips/'):
                    os.makedirs('media/trimmed_clips/')
                if not os.path.exists(f'media/trimmed_clips/{video_uuid}'):
                    os.makedirs(f'media/trimmed_clips/{video_uuid}')
                
                trimmed_clip.write_videofile(
                    f"media/trimmed_clips/{video_uuid}/{ind}.mp4",
                    codec = "libx264",
                    audio_codec = "aac",
                    threads = threads,
                    fps = clip_fps,
                    preset = 'ultrafast'
                )

                clip.close()
                trimmed_clip.close()
            
        else:
            for ind, segment in enumerate(transcript['selected_shorts']):
                clip = VideoFileClip(
                    downloaded_video_path, 
                    audio = True, 
                    target_resolution = target_resolution
                )
                clip_fps = clip.fps
                trimmed_clip = clip.subclip(segment['start'], segment['end'])

                if not os.path.exists('media/trimmed_clips/'):
                    os.makedirs('media/trimmed_clips/')
                if not os.path.exists(f'media/trimmed_clips/{video_uuid}'):
                    os.makedirs(f'media/trimmed_clips/{video_uuid}')
                
                trimmed_clip.write_videofile(
                    f"media/trimmed_clips/{video_uuid}/{ind}.mp4",
                    codec = "libx264",
                    audio_codec = "aac",
                    threads = threads,
                    fps = clip_fps,
                    preset = 'ultrafast'
                )

                clip.close()
                trimmed_clip.close()
        
        return "✅ - clips trimmed successfully"
    except Exception as e:
        return f"❗- Error trimming clips: {str(e)}"