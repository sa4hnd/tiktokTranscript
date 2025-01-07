# TikTok Transcription API

This API service allows you to transcribe TikTok videos to text using AssemblyAI.

## Quick Start for React Vite

1. **Set Up Environment Variables**
   Create `.env` file in your Vite project root:
   ```env
   # The API endpoint (required)
   VITE_API_URL=https://tiktoktranscript.fly.dev

   # Your API key (required)
   VITE_API_KEY=FjJjcJ7a9V3DtkyjnTIv9VvaU_yz5f41hntC3lkvv20
   ```

2. **Install Axios**
   ```bash
   npm install axios
   ```

3. **Make API Calls**
   ```javascript
   const response = await axios.post(
     `${import.meta.env.VITE_API_URL}/transcribe`,
     {
       tiktok_url: "YOUR_TIKTOK_URL"
     },
     {
       headers: {
         'X-API-Key': import.meta.env.VITE_API_KEY,
         'Content-Type': 'application/json'
       }
     }
   );
   ```

## API Details

### Base URL
```
https://tiktoktranscript.fly.dev
```

### Authentication
- API Key: `FjJjcJ7a9V3DtkyjnTIv9VvaU_yz5f41hntC3lkvv20`
- Add to headers as `X-API-Key`

### Endpoints

1. **Health Check**
   - `GET /`
   - No authentication required
   - Response: `{ "status": "ok", "message": "API is running" }`

2. **Transcribe Video**
   - `POST /transcribe`
   - Headers Required:
     ```json
     {
       "X-API-Key": "FjJjcJ7a9V3DtkyjnTIv9VvaU_yz5f41hntC3lkvv20",
       "Content-Type": "application/json"
     }
     ```
   - Request Body:
     ```json
     {
       "tiktok_url": "https://www.tiktok.com/@username/video/1234567890"
     }
     ```
   - Success Response (200):
     ```json
     {
       "title": "video_title",
       "transcription": "transcribed_text"
     }
     ```
   - Error Responses:
     - `400`: Invalid URL or video not accessible
     - `403`: Invalid API key
     - `500`: Server error or transcription failed

## Example Component

```jsx
import { useState } from 'react';
import axios from 'axios';

const TranscriptionComponent = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleTranscribe = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/transcribe`,
        {
          tiktok_url: url
        },
        {
          headers: {
            'X-API-Key': import.meta.env.VITE_API_KEY,
            'Content-Type': 'application/json'
          }
        }
      );

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter TikTok URL"
      />
      <button onClick={handleTranscribe} disabled={loading}>
        {loading ? 'Transcribing...' : 'Transcribe'}
      </button>
      {error && <div style={{color: 'red'}}>{error}</div>}
      {result && (
        <div>
          <h3>Title: {result.title}</h3>
          <p>{result.transcription}</p>
        </div>
      )}
    </div>
  );
};

export default TranscriptionComponent;
```

## Important Notes

1. **Environment Variables**
   - Must start with `VITE_` to be exposed to client code
   - Required variables:
     ```env
     VITE_API_URL=https://tiktoktranscript.fly.dev
     VITE_API_KEY=FjJjcJ7a9V3DtkyjnTIv9VvaU_yz5f41hntC3lkvv20
     ```

2. **URL Format**
   - Must be a valid TikTok URL
   - Format: `https://www.tiktok.com/@username/video/1234567890`

3. **Rate Limiting**
   - Consider implementing rate limiting in your frontend
   - API has a timeout of 30 seconds for transcription

4. **Error Handling**
   ```javascript
   try {
     const response = await axios.post(...);
   } catch (error) {
     if (error.response?.status === 403) {
       // Handle invalid API key
     } else if (error.response?.status === 400) {
       // Handle invalid URL
     } else {
       // Handle other errors
     }
   }
   ```
