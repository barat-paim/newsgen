import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Share2, ThumbsUp, ThumbsDown, HelpCircle, Star, Power, Lock, PowerSquareIcon, SwissFranc, RulerIcon, CarrotIcon, LucideCarrot, BoxesIcon, FrownIcon, PiIcon, DotIcon, CreativeCommonsIcon, ActivityIcon, SquareDotIcon, LucideMoveDiagonal2, CpuIcon, HazeIcon, Activity } from 'lucide-react';
import { Switch } from './components/ui/switch';
import { ClipLoader } from 'react-spinners';

const VariantBox = ({ number }) => (
  <div className="w-8 h-8 border border-gray-600 rounded flex items-center justify-center text-gray-400">
    {number}
  </div>
);

const NewsFunApp = () => {
  const [articleText, setArticleText] = useState('');
  const [cartoon, setCartoon] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [concept, setConcept] = useState('');
  const [loadingMessage, setLoadingMessage] = useState('');
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const [memoryEnabled, setMemoryEnabled] = useState(false);
  const [timeoutIds, setTimeoutIds] = useState([]);

  useEffect(() => {
    if (isLoading) {
      const loadingMessages = ['Loading...', 'Generating cartoon...'];
      loadingMessages.forEach((message, index) => {
        const timeout = setTimeout(() => {
          setLoadingMessage(message);
        }, index * 10000);
        timeoutIds.push(timeout);
      });
    } else {
      setLoadingMessage('');
      }
  }, [isLoading]);

  const generateCartoon = async () => {
    setIsLoading(true);
    setError('');
    setCartoon('');
    setConcept('');
    setLoadingMessage('');

    try {
      console.log('Sending request to generate cartoon');
      const response = await axios.post('/api/generate_cartoon', 
        { article_text: articleText },
        { 
          headers: {
            'Content-Type': 'application/json',
          }
        }
      );
      console.log('API response:', response.data);
      if (response.data.error) {
        setError(response.data.error);
      } else if (response.data.image_url) {
        setCartoon(response.data.image_url);
        setConcept(response.data.caption);
      } else {
        setError('Unexpected response from server. Please try again.');
      }
    } catch (err) {
      console.error('Error generating cartoon:', err);
      setError('Failed to generate. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-neutral-950 text-white">
      <header className="p-2 flex justify-left">
        <h1 className="flex-grow mt-2 text-2xl text-gray-400 font-light tracking-tight pl-4">
          <span className="font-semibold">Generative Strips</span>
        </h1>
      </header>
      
      <div className="flex flex-col md:flex-row flex-1 p-4 space-y-4 md:space-y-0 md:space-x-2">
        <aside className="w-full md:w-1/4 bg-neutral-700 border border-black p-4 flex flex-col">
          <div className="flex-grow">
            <textarea 
              className="w-full h-40 md:h-full p-2 bg-transparent border border-black text-neutral-400 rounded-xl pl-4 focus:border-gray-500 focus:outline-none" 
              placeholder="paste article text here..."
              value={articleText}
              onChange={(e) => setArticleText(e.target.value)}
            />
          </div>
          <button 
            className="w-full p-2 mt-4 rounded-xl bg-gradient-to-r from-[#F9AD7C] via-[#F9C0F2] to-[#8DF9F9] text-black font-semibold text-xl text-center transition-all duration-300 hover:scale-105"
            onClick={generateCartoon}
            disabled={isLoading}
            style={{ lineHeight: '1' }}
          >
            {isLoading ? 'creating...' : (
              <>
                <Activity className="inline w-4 h-4 mr-2" />
                create
              </>
            )}
          </button>
          
          {/* Beta Features section */}
          <div className="mt-6 pt-4 border-t border-gray-700">
            <h2 className="text-sm font-semibold text-gray-400 mb-4 flex items-center">
              <Lock className="w-4 h-4 mr-1" />
              Beta Features
            </h2>
            <div className="space-y-4 opacity-60">
              <div>
                <label className="block text-sm font-medium text-white mb-2">Variants</label>
                <div className="flex space-x-2">
                  <VariantBox number={1} />
                  <VariantBox number={2} />
                  <VariantBox number={3} />
                  <VariantBox number={4} />
                </div>
              </div>
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-white">Character Voice</label>
                <Switch 
                  checked={voiceEnabled} 
                  onCheckedChange={setVoiceEnabled}
                  disabled
                />
              </div>
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-white">Character Memory</label>
                <Switch 
                  checked={memoryEnabled} 
                  onCheckedChange={setMemoryEnabled}
                  disabled
                />
              </div>
            </div>
          </div>
        </aside>
        
        <main className="flex-1 bg-neutral-800 border border-black p-4 min-h-[300px]">
          {isLoading ? (
            <div className="flex flex-col items-center justify-center h-full">
              <div className="loader"></div>
              <p className="mt-4 text-gray-500">Loading...</p>
            </div>
          ) : cartoon ? (
            <img src={cartoon} alt="Generated Cartoon" className="max-w-full h-auto max-h-[300px] object-contain" />
          ) : (
            <div className="h-full flex items-center justify-center text-gray-500">
              your comic strip will appear here...
            </div>
          )}
          {concept && <p className="mt-2"><strong>Caption:</strong> 'test'</p>}
        </main>
      </div>
    </div>
  );
};

export default NewsFunApp;