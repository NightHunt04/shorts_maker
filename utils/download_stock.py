from utils.fetch_stock import fetch_stock
import requests, random, os

def download_stock(video_uuid, words, idx, media = 'image', orientation = 'portrait'):
    try:
        for ind, word in enumerate(words):
            response = fetch_stock(media, word, orientation)
            if response:
                image_url = response['photos'][random.randint(0, len(response['photos']) - 2)]['src']['portrait']
                stream_response = requests.get(image_url, stream = True)

                if not os.path.exists('media/stock_media/'):
                    os.mkdir('media/stock_media/')
                if not os.path.exists(f'media/stock_media/{video_uuid}'):
                    os.mkdir(f'media/stock_media/{video_uuid}')
                if not os.path.exists(f'media/stock_media/{video_uuid}/{idx}'):
                    os.mkdir(f'media/stock_media/{video_uuid}/{idx}')

                if stream_response.status_code == 200:
                    with open(f'media/stock_media/{video_uuid}/{idx}/{ind}.jpg', 'wb') as file:
                        for chunk in stream_response.iter_content(chunk_size=1024): 
                            file.write(chunk)
                    print(f'✅ stock word: {word} - image downloaded')
                else:
                    print('Failed to download image:', stream_response.status_code)
        return "✅ - stock images downloaded successfully"
    except Exception as e:
        return f"❗- Error downloading stock images: {str(e)}"

