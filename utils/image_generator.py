from groq import Groq
import os
import requests
from dotenv import load_dotenv
load_dotenv()

def image_generator(idx, words, video_uuid):
    groq = Groq(max_retries = 3)

    for ind, word in enumerate(words):  
        try:
            img_prompt = groq.chat.completions.create(
                model = 'llama3-8b-8192',
                messages = [
                    {
                        "role": "system",
                        "content": "Your task is to generate a detailed and enhanced prompt for generating images from given word by the user. The prompt should be specific, informative, and tailored to the user's input word. The generated prompt should guide the image-generation model in generating high-quality images that capture the essence of the input word. The output must only contain the prompt and no other text or punctuation or else you get penalized."
                    },
                    {
                        "role": "user",
                        "content": f"Given word: {word}"
                    }
                ],
                temperature = 1,
                max_tokens = 500,
                top_p = 1,
                stop = None,
            )
            img_prompt = img_prompt.choices[0].message.content
            width = 405
            height = 720
            params = {
                'width': width,
                'height': height,
                'nologo': 'true',
                'private': 'true',
                'enhance': 'true'
            }
            pollinations_base_url = "https://image.pollinations.ai/prompt/"

            url = f"{pollinations_base_url}{requests.utils.quote(img_prompt)}"

            response = requests.get(url, params=params, timeout=(10, 600))
            response.raise_for_status()

            if not os.path.exists(f'media/stock_media'):
                os.mkdir('media/stock_media')
            if not os.path.exists(f'media/stock_media/{video_uuid}'):
                os.mkdir(f'media/stock_media/{video_uuid}')
            if not os.path.exists(f'media/stock_media/{video_uuid}/{idx}'):
                os.mkdir(f'media/stock_media/{video_uuid}/{idx}')
                
            with open(f'media/stock_media/{video_uuid}/{idx}/{ind}.jpg', 'wb') as file:
                file.write(response.content)
            print(f'✅ - word: {word} - ai generated image downloaded')
        
        except Exception as e:
            return f'❗ - word: {word} - ai generated image downloading failed: {str(e)}'

    return "✅ - all ai generated images downloaded successfully"
