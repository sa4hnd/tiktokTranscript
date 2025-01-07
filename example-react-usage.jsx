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
      
      const response = await axios.post('http://localhost:8000/transcribe', {
        tiktok_url: url,
        save_transcript: true
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <div className="mb-4">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter TikTok URL"
          className="w-full p-2 border rounded"
        />
      </div>

      <button
        onClick={handleTranscribe}
        disabled={loading || !url}
        className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
      >
        {loading ? 'Transcribing...' : 'Transcribe'}
      </button>

      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-4">
          <h3 className="font-bold">Title: {result.title}</h3>
          <p className="mt-2 whitespace-pre-wrap">{result.transcription}</p>
          {result.file_path && (
            <p className="mt-2 text-sm text-gray-600">
              Saved to: {result.file_path}
            </p>
          )}
        </div>
      )}
    </div>
  );
}; 