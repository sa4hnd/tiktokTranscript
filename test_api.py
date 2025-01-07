import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# The URL of your API endpoint (use environment variable or default to localhost)
api_url = os.getenv("API_URL", "http://localhost:8000") + "/transcribe"

# Get API key from environment
api_key = os.getenv("API_KEY")

print(f"\nUsing API at: {api_url}")

# The TikTok video URL you want to transcribe (replace with your TikTok URL)
tiktok_url = input("\nEnter TikTok URL: ")

# Request payload
payload = {
    "tiktok_url": tiktok_url,
    "save_transcript": True
}

# Headers with API key
headers = {
    "X-API-Key": api_key,
    "Content-Type": "application/json"
}

# Make the POST request
try:
    print("\nTranscribing video...")
    response = requests.post(api_url, json=payload, headers=headers)
    
    # Check if request was successful
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Transcription successful!")
        print(f"\nVideo title: {result['title']}")
        print(f"\nTranscription:\n{result['transcription']}")
        if result['file_path']:
            print(f"\nSaved to file: {result['file_path']}")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.json())
        
except Exception as e:
    print(f"\n❌ Error occurred: {str(e)}") 