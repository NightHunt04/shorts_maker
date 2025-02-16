import os
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import cv2
import numpy as np

def curve_mask(video_uuid, threads, cinematic_crop_background):
    try:
        if not os.path.exists('media/cropped_clips/'):
            os.mkdir('media/cropped_clips/')
        if not os.path.exists(f'media/cropped_clips/{video_uuid}'):
            os.mkdir(f'media/cropped_clips/{video_uuid}')
        
        for ind in range(len(os.listdir(f'media/trimmed_clips/{video_uuid}'))):
            input_path = f"media/trimmed_clips/{video_uuid}/{ind}.mp4"
            output_path = f"media/cropped_clips/{video_uuid}/{ind}.mp4"

            video = VideoFileClip(input_path)

            final_height = 1920
            final_width = int(final_height * (9 / 16))

            if cinematic_crop_background.strip() == 'black':
                black_bg = ImageClip(np.zeros((final_height, final_width, 3), dtype=np.uint8), duration=video.duration)
            elif cinematic_crop_background.strip() == 'white':
                black_bg = ImageClip(np.ones((final_height, final_width, 3), dtype=np.uint8) * 255, duration=video.duration)

            video_width, video_height = video.size
            gap = 40  
            new_video_width = final_width - 2 * gap  
            scale_factor = new_video_width / video_width
            new_video_height = int(video_height * scale_factor)

            video_resized = video.resize(height=new_video_height, width=new_video_width)

            mask = np.zeros((new_video_height, new_video_width, 3), dtype=np.uint8)
            radius = 30 

            cv2.rectangle(mask, (radius, 0), (new_video_width - radius, new_video_height), (255, 255, 255), -1)
            cv2.rectangle(mask, (0, radius), (new_video_width, new_video_height - radius), (255, 255, 255), -1)
            cv2.circle(mask, (radius, radius), radius, (255, 255, 255), -1)
            cv2.circle(mask, (new_video_width - radius, radius), radius, (255, 255, 255), -1)
            cv2.circle(mask, (radius, new_video_height - radius), radius, (255, 255, 255), -1)
            cv2.circle(mask, (new_video_width - radius, new_video_height - radius), radius, (255, 255, 255), -1)

            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY) / 255.0
            mask_clip = ImageClip(mask, ismask=True).set_duration(video.duration)
            rounded_video = video_resized.set_mask(mask_clip)
            final_clip = CompositeVideoClip([black_bg, rounded_video.set_position("center")])

            final_clip.write_videofile(
                output_path, 
                fps=video.fps,
                codec = 'libx264',
                audio_codec = 'aac',
                threads = threads,
                preset = 'ultrafast'
            )
            print(f"✅ - [{ind}] clip resized successfully")

        return "✅ - all clips resized successfully"
    except Exception as e:
        return f"❗- Error resizing clips: {str(e)}"
