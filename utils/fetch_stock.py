import requests, json, os
from dotenv import load_dotenv
load_dotenv()

def fetch_stock(media, query, orientation = 'portrait'):
    BASE_URL = os.getenv("PEXELS_BASE_URL")
    endpoint = '/api/pexels'

    if media == 'image':
        endpoint += '-photo'
    
    payload = json.dumps({
        "query": query,
        "orientation": orientation
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        url = BASE_URL + endpoint
        response = requests.request('POST', url, headers = headers, data = payload)
        return response.json()
    except Exception as e:
        print(e)
    
