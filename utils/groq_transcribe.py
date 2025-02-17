from groq import Groq
from utils.make_audio_file import make_single_audio_file
from dotenv import load_dotenv
load_dotenv()
import os

def groq_transcribe(video_uuid, language = 'en'):
    groq = Groq(max_retries = 3)

    try:
        make_single_audio_file(f'media/downloads/{video_uuid}.mp4', video_uuid)
        audio_path = f"media/audio_files/{video_uuid}.mp3"
        with open(audio_path, 'rb') as audio_file:
            transcription = groq.audio.transcriptions.create(
                file = audio_file,
                model = 'whisper-large-v3-turbo',
                language = language,
                response_format = 'verbose_json'
            )
            print(transcription.segments)
            return transcription.segments, "✅ - transcript created successfully"
    except Exception as e:
        return None, f"❗- Error transcribing video: {str(e)}"

# groq_transcribe('e40519a1-0fcd-49b2-9a06-3aa1b26967ab')