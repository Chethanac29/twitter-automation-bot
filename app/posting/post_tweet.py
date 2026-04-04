import requests
from dotenv import load_dotenv
import os
load_dotenv()

# Use the 60-day token here
ACCESS_TOKEN = os.environ.get("THREADS_API_KEY")

def post_to_threads(text_content):
    # Part A: Create the Media Container (Text only)
    # 'me' refers to the account the token belongs to
    create_url = "https://graph.threads.net/v1.0/me/threads"
    payload = {
        'media_type': 'TEXT',
        'text': text_content,
        'access_token': ACCESS_TOKEN
    }
    
    res = requests.post(create_url, data=payload)
    container_id = res.json().get('id')
    
    if not container_id:
        print("Failed to create container:", res.json())
        return

    # Part B: Publish the Container
    publish_url = "https://graph.threads.net/v1.0/me/threads_publish"
    publish_payload = {
        'creation_id': container_id,
        'access_token': ACCESS_TOKEN
    }
    
    final_res = requests.post(publish_url, data=publish_payload)
    print("Successfully posted! ID:", final_res.json().get('id'))
