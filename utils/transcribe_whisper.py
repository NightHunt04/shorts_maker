import whisper

def transcribe_whisper(audio, language = 'en'):
    try:
        model = whisper.load_model("tiny")
        result = model.transcribe(audio, word_timestamps = True, language = language)
        return result, "✅ - transcript created successfully"
    except Exception as e:
        return None, f"❗- Error transcribing audio: {str(e)}"