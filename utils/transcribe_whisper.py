import whisper

def transcribe_whisper(audio):
    try:
        model = whisper.load_model("tiny")
        result = model.transcribe(audio, word_timestamps = True)
        return result, "✅ - transcript created successfully"
    except Exception as e:
        return None, f"❗- Error transcribing audio: {str(e)}"