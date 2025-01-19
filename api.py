from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, HttpUrl
import yt_dlp
import os
import re
import assemblyai as aai
from typing import Optional
from dotenv import load_dotenv
from starlette.status import HTTP_403_FORBIDDEN

# Load environment variables
load_dotenv()

# API Keys and Config
API_KEY = os.getenv("API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5173",  # Vite default port
    "http://localhost:8081",  # Added new localhost port
    "http://127.0.0.1:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8081",  # Added new localhost port
    "https://nodeflowai.com",  # Added production domain
]

# Setup AssemblyAI
aai.settings.api_key = ASSEMBLYAI_API_KEY

app = FastAPI(title="TikTok Transcription API")

# Add health check endpoint
@app.get("/")
async def health_check():
    return {"status": "ok", "message": "API is running"}

# Security
api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate API key"
    )

# Add CORS middleware with more permissive settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class TranscriptionRequest(BaseModel):
    tiktok_url: str
    save_transcript: Optional[bool] = False

    def validate_tiktok_url(self):
        if not re.match(r'https?://(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+', self.tiktok_url):
            raise ValueError("Invalid TikTok URL format")

class TranscriptionResponse(BaseModel):
    title: str
    transcription: str
    file_path: Optional[str] = None

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_tiktok(
    request: TranscriptionRequest,
    api_key: str = Depends(get_api_key)
):
    try:
        # Validate TikTok URL
        request.validate_tiktok_url()

        # Get video title
        try:
            with yt_dlp.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(request.tiktok_url, download=False)
                video_title = info_dict.get('title', None)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail="Failed to fetch video information. Please check if the URL is correct and the video is accessible."
            )

        sanitized_video_title = re.sub(r'#\w+\s*', '', video_title) if video_title else 'my_tiktok'
        sanitized_video_title = re.sub(r'[\/:*?"<>|]', '_', sanitized_video_title)

        # Setup directories
        work_dir = 'work'
        transcripts_dir = 'transcripts'
        os.makedirs(work_dir, exist_ok=True)
        if request.save_transcript:
            os.makedirs(transcripts_dir, exist_ok=True)

        # Download audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0',
            }],
            'outtmpl': os.path.join(work_dir, f'{sanitized_video_title}.%(ext)s'),
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([request.tiktok_url])
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail="Failed to download audio. The video might be private or deleted."
            )

        mp3_file_path = os.path.join(work_dir, f'{sanitized_video_title}.mp3')

        # Transcribe using AssemblyAI
        try:
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(mp3_file_path)
            transcription = transcript.text
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Transcription failed. Please try again later."
            )

        # Save transcript if requested
        file_path = None
        if request.save_transcript:
            file_path = os.path.join(transcripts_dir, f'{sanitized_video_title}.txt')
            with open(file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(transcription)

        # Cleanup
        try:
            os.remove(mp3_file_path)
        except:
            pass  # Ignore cleanup errors

        return TranscriptionResponse(
            title=sanitized_video_title,
            transcription=transcription,
            file_path=file_path
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 