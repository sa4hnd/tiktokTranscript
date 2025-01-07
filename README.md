# TikTok Transcription API

This API service allows you to transcribe TikTok videos to text using AssemblyAI.

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your AssemblyAI API key (get it from [AssemblyAI](https://www.assemblyai.com/))
   - Set your API key for authentication
   - Configure allowed origins

## API Endpoint

### Transcribe TikTok Video

**Endpoint:** `POST /transcribe`

**Headers:**
```
X-API-Key: your-api-key
Content-Type: application/json
```

**Request Body:**
```json
{
    "tiktok_url": "https://www.tiktok.com/@username/video/1234567890",
    "save_transcript": true  // optional, defaults to false
}
```

**Response:**
```json
{
    "title": "video_title",
    "transcription": "transcribed_text",
    "file_path": "path_to_saved_file"  // only if save_transcript is true
}
```

**Error Responses:**
- `400`: Invalid URL or video not accessible
- `403`: Invalid API key
- `500`: Server error or transcription failed

## Running the API

1. Start the server:
```bash
python api.py
```
2. API will be available at `http://localhost:8000`
3. Access API documentation at `http://localhost:8000/docs`

## React Integration

1. Copy `.env.example` to `.env` in your React project
2. Set your environment variables:
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_KEY=your-api-key
```
3. Import and use the TranscriptionComponent:
```jsx
import TranscriptionComponent from './components/TranscriptionComponent';

function App() {
  return (
    <div>
      <TranscriptionComponent />
    </div>
  );
}
```

## Example cURL Request

```bash
curl -X POST http://localhost:8000/transcribe \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "tiktok_url": "https://www.tiktok.com/@username/video/1234567890",
    "save_transcript": true
  }'
```

## Files Structure

```
├── api.py              # Main API server
├── .env               # Environment variables
├── requirements.txt   # Python dependencies
└── example-react-usage.jsx  # React component example
```

## Notes

- The API requires a valid TikTok video URL
- Transcripts are saved in the `transcripts` directory when `save_transcript` is true
- Temporary files are automatically cleaned up after transcription
