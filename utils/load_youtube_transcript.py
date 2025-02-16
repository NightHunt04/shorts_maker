from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat

def load_youtube_transcript(url, shorts_length = 60):
    try:
        loader = YoutubeLoader.from_youtube_url(
            url, 
            add_video_info = False,
            transcript_format = TranscriptFormat.CHUNKS,
            chunk_size_seconds = shorts_length
        )
        data = loader.load()
        return data, "✅ - transcript loaded successfully"
    except Exception as e:
        return None, f"❗- Error loading transcript: {str(e)}"