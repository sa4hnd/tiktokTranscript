import requests

# The URL of your API endpoint
api_url = "http://localhost:8000/transcribe"

# The TikTok video URL you want to transcribe
tiktok_url = "https://www.tiktok.com/@username/video/1234567890"  # Replace with your TikTok URL

# Request payload
payload = {
    "tiktok_url": tiktok_url,
    "save_transcript": True
}

# Make the POST request
try:
    response = requests.post(api_url, json=payload)
    
    # Check if request was successful
    if response.status_code == 200:
        result = response.json()
        print("Transcription successful!")
        print(f"Video title: {result['title']}")
        print(f"Transcription: {result['transcription']}")
        if result['file_path']:
            print(f"Saved to file: {result['file_path']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        
except Exception as e:
    print(f"Error occurred: {str(e)}") 