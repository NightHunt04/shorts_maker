from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

video = VideoFileClip('../media/final_clips/4db51ad0-11d4-454e-8180-a39244dee0f3/0.mp4')
music = AudioFileClip('../music/Echo-Sax-End.mp3')

video_audio = AudioFileClip('../media/audio_files/4db51ad0-11d4-454e-8180-a39244dee0f3/0.mp3')
video_audio_duration = video_audio.duration
music = music.set_duration(video_audio_duration).volumex(0.36)

new_audio = CompositeAudioClip([video_audio, music])

video = video.set_audio(new_audio)
video.write_videofile('OUTPUT5.mp4')