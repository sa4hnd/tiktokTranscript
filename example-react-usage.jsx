import { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_KEY = process.env.REACT_APP_API_KEY;

const TranscriptionComponent = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const validateTikTokUrl = (url) => {
    const pattern = /^https?:\/\/(?:www\.)?tiktok\.com\/@[\w.-]+\/video\/\d+/;
    return pattern.test(url);
  };

  const handleTranscribe = async () => {
    try {
      // Validate URL format
      if (!validateTikTokUrl(url)) {
        setError('Please enter a valid TikTok video URL');
        return;
      }

      setLoading(true);
      setError(null);
      
      const response = await axios.post(`${API_URL}/transcribe`, 
        {
          tiktok_url: url,
          save_transcript: true
        },
        {
          headers: {
            'X-API-Key': API_KEY,
            'Content-Type': 'application/json'
          }
        }
      );

      setResult(response.data);
    } catch (err) {
      console.error('Transcription error:', err);
      
      if (err.response?.status === 403) {
        setError('Authentication failed. Please check your API key.');
      } else if (err.response?.status === 400) {
        setError(err.response.data.detail || 'Invalid request. Please check the video URL.');
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else if (!navigator.onLine) {
        setError('Network error. Please check your internet connection.');
      } else {
        setError('An error occurred while transcribing the video. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">TikTok Video Transcription</h1>
      
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">
          TikTok Video URL
        </label>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://www.tiktok.com/@username/video/1234567890"
          className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <button
        onClick={handleTranscribe}
        disabled={loading || !url}
        className="w-full px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? (
          <span className="flex items-center justify-center">
            <svg className="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Transcribing...
          </span>
        ) : (
          'Transcribe'
        )}
      </button>

      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded border border-red-200">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-6 p-4 bg-gray-50 rounded">
          <h3 className="font-bold text-lg mb-2">Title: {result.title}</h3>
          <div className="bg-white p-4 rounded border">
            <p className="whitespace-pre-wrap">{result.transcription}</p>
          </div>
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