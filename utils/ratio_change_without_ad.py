from moviepy.editor import VideoFileClip, CompositeVideoClip
import numpy as np
from skimage.filters import gaussian
import skimage
import os

def apply_gaussian_blur(get_frame, t):
    frame = get_frame(t)
    frame_normalized = frame.astype(np.float32) / 255.0
    if skimage.__version__ >= '0.19':
        blurred_frame = gaussian(frame_normalized, sigma=10, channel_axis=-1)
    else:
        blurred_frame = gaussian(frame_normalized, sigma=10, multichannel=True)
    return (blurred_frame * 255).astype(np.uint8)

def resize_frame(video_uuid, THREADS_TO_BE_USED):
    try:
        if not os.path.exists('media/cropped_clips/'):
            os.mkdir('media/cropped_clips/')
        if not os.path.exists(f'media/cropped_clips/{video_uuid}'):
            os.mkdir(f'media/cropped_clips/{video_uuid}')
        
        for ind in range(len(os.listdir(f'media/trimmed_clips/{video_uuid}'))):
            input_path = f"media/trimmed_clips/{video_uuid}/{ind}.mp4"
            output_path = f"media/cropped_clips/{video_uuid}/{ind}.mp4"
            video = VideoFileClip(input_path)

            # Downscale the video to reduce memory usage (e.g., to 720p)
            target_height = 1920

            # Calculate target dimensions for 9:16 aspect ratio
            target_width = int((9 / 16) * target_height)

            # Resize and blur the background video
            bg_video = video.resize(height=target_height)
            bg_video = bg_video.crop(x_center=bg_video.w / 2, width=target_width)
            bg_video = bg_video.fl(apply_gaussian_blur).set_opacity(0.4)

            # Resize the foreground video to fit within the 9:16 frame
            scale_factor = target_width / video.w
            foreground_video = video.resize(scale_factor)

            # Center the foreground video on the blurred background
            final_video = CompositeVideoClip([bg_video, foreground_video.set_position("center")])
            final_video.write_videofile(
                output_path, 
                codec="libx264", 
                audio_codec="aac",
                preset="ultrafast",
                threads=THREADS_TO_BE_USED,
                fps=video.fps
            )

            video.close()
            bg_video.close()
            foreground_video.close()
            final_video.close()

            print(f"✅ - [{ind}] clip resized successfully")
        return "✅ - all clips resized successfully"
    except Exception as e:
        return f"❗- Error resizing clips: {str(e)}"
