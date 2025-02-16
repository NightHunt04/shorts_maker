def format_youtube_transcript(transcript, short_length = 60):
    try:
        formatted_transcript = []

        for document in transcript:
            start_seconds = document.metadata['start_seconds']
            page_content = document.page_content
            formatted_transcript.append({ 'text': page_content, 'start': start_seconds, 'end': start_seconds + short_length })

        return formatted_transcript, "✅ - transcript formatted successfully"
    except Exception as e:
        return None, f"❗- Error formatting transcript: {str(e)}"