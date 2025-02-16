import numpy as np
from moviepy.editor import VideoFileClip
from ultralytics import YOLO 
from collections import deque
import os 

class SmoothingBuffer:
    def __init__(self, buffer_size=30, change_threshold=150):
        self.buffer_size = buffer_size
        self.change_threshold = change_threshold
        self.positions = deque(maxlen=buffer_size)
        self.last_center = None

    def update(self, center_x):
        if self.last_center is not None:
            if abs(center_x - self.last_center) > self.change_threshold:
                self.positions.clear()

        self.positions.append(center_x)
        self.last_center = center_x

    def get_smooth_position(self):
        if not self.positions:
            return None
        weights = np.linspace(0.5, 1.0, len(self.positions))
        weights = weights / weights.sum()
        return np.average(list(self.positions), weights=weights)

def get_human_centers(detections):
    centers = []
    for box in detections:
        center_x = (box[0] + box[2]) / 2
        centers.append(center_x)
    return centers

def get_crop(frame, center_x, target_ratio=9/16):
    height, width = frame.shape[:2]
    new_width = int(height * target_ratio)

    if center_x is None:
        left = (width - new_width) // 2
    else:
        left = int(center_x - new_width / 2)

        if left < 0:
            left = 0
        elif left + new_width > width:
            left = width - new_width

    return frame[:, left:left+new_width]

def process_video(index, input_path, output_path, THREADS_TO_BE_USED):
    model = YOLO('models/yolov8n.pt')
    video = VideoFileClip(input_path)

    frame_count = 0
    last_humans = []
    smoothing_buffer = SmoothingBuffer()
    human_index = 0  
    cycle_interval = 275  

    def process_frame(frame):
        nonlocal frame_count, last_humans, human_index

        center_x = None

        if frame_count % 24 == 0:
            results = model(frame, classes=[0], conf=0.5)
            detected_boxes = []
            for r in results:
                if len(r.boxes) > 0:
                    boxes = r.boxes.xyxy.cpu().numpy()
                    classes = r.boxes.cls.cpu().numpy()
                    for box, cls in zip(boxes, classes):
                        if cls == 0:  # person
                            detected_boxes.append(box)

            last_humans = detected_boxes

        if last_humans:
            centers = get_human_centers(last_humans)
            if centers:
                if len(centers) == 1:
                    center_x = centers[0]
                    smoothing_buffer.update(center_x)
                    center_x = smoothing_buffer.get_smooth_position()
                else:
                    center_x = centers[human_index % len(centers)]
                    smoothing_buffer.update(center_x)
                    center_x = smoothing_buffer.get_smooth_position()

                    if frame_count % cycle_interval == 0:
                        human_index += 1

        frame_count += 1

        cropped_frame = get_crop(frame, center_x)

        return cropped_frame

    processed_video = video.fl_image(process_frame)
    final_height = 1920
    scale_factor = final_height / video.h
    processed_video = processed_video.resize(scale_factor)

    processed_video.write_videofile(
        output_path, 
        audio=True, 
        threads=THREADS_TO_BE_USED, 
        codec="libx264", 
        audio_codec="aac",
        fps=video.fps,
        preset='ultrafast'
    )

    video.close()
    processed_video.close()
    return f"✅ - cropped video [{index}] saved at {output_path}"

def auto_detect_humans(video_uuid, THREADS_TO_BE_USED):
    if not os.path.exists('media/cropped_clips/'):
        os.mkdir('media/cropped_clips/')
    if not os.path.exists(f'media/cropped_clips/{video_uuid}'):
        os.mkdir(f'media/cropped_clips/{video_uuid}')
    
    try:
        for ind in range(len(os.listdir(f'media/trimmed_clips/{video_uuid}'))):
            status = process_video(ind, f'media/trimmed_clips/{video_uuid}/{ind}.mp4', f'media/cropped_clips/{video_uuid}/{ind}.mp4', THREADS_TO_BE_USED)
            print(status)
    except Exception as e:
        return f"❗- Error auto detecting humans: {str(e)}"
