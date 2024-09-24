import React, { useState } from 'react';
import axios from 'axios';

const NewsAudioGen = () => {
  const [articleText, setArticleText] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [script, setScript] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const generateNewsAudio = async () => {
    setIsLoading(true);
    setError('');
    setAudioUrl('');
    setScript('');

    try {
      const response = await axios.post('/api/generate_news_audio', 
        { article_text: articleText },
        { 
          headers: {
            'Content-Type': 'application/json',
          }
        }
      );
      if (response.data.error) {
        setError(response.data.error);
      } else if (response.data.audio_url) {
        setAudioUrl(response.data.audio_url);
        setScript(response.data.script);
      } else {
        setError('Unexpected response from server. Please try again.');
      }
    } catch (err) {
      console.error('Error generating news audio:', err);
      setError('Failed to generate. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-neutral-950 text-white p-4">
      <h1 className="text-2xl font-semibold mb-4">News Audio Generator</h1>
      <textarea 
        className="w-full h-40 p-2 bg-neutral-800 border border-gray-600 text-white rounded-xl mb-4"
        placeholder="Paste article text here..."
        value={articleText}
        onChange={(e) => setArticleText(e.target.value)}
      />
      <button 
        className="w-full p-2 rounded-xl bg-blue-600 text-white font-semibold text-xl mb-4"
        onClick={generateNewsAudio}
        disabled={isLoading}
      >
        {isLoading ? 'Generating...' : 'Generate News Audio'}
      </button>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      {audioUrl && (
        <div className="mb-4">
          <h2 className="text-xl font-semibold mb-2">Generated Audio:</h2>
          <audio controls src={audioUrl} className="w-full" />
        </div>
      )}
      {script && (
        <div>
          <h2 className="text-xl font-semibold mb-2">Generated Script:</h2>
          <pre className="whitespace-pre-wrap bg-neutral-800 p-4 rounded">{script}</pre>
        </div>
      )}
    </div>
  );
};

export default NewsAudioGen;