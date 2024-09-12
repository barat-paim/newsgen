import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Share2, ThumbsUp, ThumbsDown, HelpCircle } from 'lucide-react';

const NewsFunApp = () => {
  const [articleText, setArticleText] = useState('');
  const [cartoon, setCartoon] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [concept, setConcept] = useState('');
  const [loadingMessage, setLoadingMessage] = useState('');

  const loadingMessages = [
    "Putting our best cartoonist to work...",
    "Generating cartoon...",
    "Our chief editor approves.."
  ];

  useEffect(() => {
    const timeouts = [];
    if (isLoading) {
      loadingMessages.forEach((message, index) => {
        const timeout = setTimeout(() => {
          setLoadingMessage(message);
        }, index * 10000);
        timeouts.push(timeout);
      });
    } else {
      setLoadingMessage('');
    }

    return () => {
      timeouts.forEach(clearTimeout);
    };
  }, [isLoading]);

  const generateCartoon = async () => {
    setIsLoading(true);
    setError('');
    try {
      console.log('Sending request to generate cartoon');
      const response = await axios.post('http://localhost:5000/api/generate_cartoon', 
        { article_text: articleText },
        { 
          headers: {
            'Content-Type': 'application/json',
          },
          withCredentials: true
        }
      );
      console.log('API response:', response.data);
      // This shows the cartoon image in the browser 
      setCartoon(response.data.image_url); // Set the cartoon image URL
      // Assuming the backend returns a caption
      setConcept(response.data.caption);
      
    } catch (err) {
      console.error('Error generating cartoon:', err);
      setError('Failed to generate cartoon. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full mx-auto p-4 font-sans min-h-screen flex flex-col">
      <header className="p-4 relative">
        <h1 className="text-4xl font-bold text-gray-700 text-center">
          <span className="bg-black text-white px-1 py-0.5">make news fun</span>
        </h1>
        <HelpCircle className="absolute top-4 right-4 text-gray-500 cursor-pointer" />
      </header>
      <div className="flex flex-col md:flex-row bg-gray-100 rounded-lg overflow-hidden w-full flex-grow">
        <div className="w-full md:w-1/5 p-6 bg-gray-200">
          <textarea 
            className="w-full h-64 p-4 text-lg rounded border border-gray-300" 
            placeholder="paste your article text here"
            value={articleText}
            onChange={(e) => setArticleText(e.target.value)}
          />
          <button 
            className="w-full mt-4 bg-black text-white py-2 px-2 rounded-full"
            onClick={generateCartoon}
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <span className="mr-2">Generating...</span>
                <div className="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              </div>
            ) : 'Generate'}
          </button>
        </div>
        <div className="w-full md:w-4/5 p-6 bg-gray-300 flex flex-col justify-between">
          <div className="flex-grow bg-white rounded flex items-center justify-center p-4">
            {isLoading ? (
              <p className="text-gray-500">{loadingMessage}</p>
            ) : error ? (
              <p className="text-red-500">{error}</p>
            ) : cartoon ? (
              <img src={cartoon} alt="Generated Cartoon" className="max-w-full max-h-full object-contain" />
            ) : (
              <p className="text-gray-500">Your cartoon will appear here</p>
            )}
          </div>
          {concept && <p className="mt-2"><strong>Caption:</strong> {concept}</p>}
          {prompt && <p className="mt-2"><strong>Prompt:</strong> {prompt}</p>}
          <div className="flex justify-between items-center mt-4">
            <div className="flex space-x-2">
              <ThumbsUp className="cursor-pointer" />
              <ThumbsDown className="cursor-pointer" />
            </div>
            <Share2 className="cursor-pointer" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default NewsFunApp;