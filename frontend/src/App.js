import React, { useState } from 'react';
import NewsFunApp from './NewsFunApp';
import NewsAudioGen from './NewsAudioGen';

const App = () => {
  const [activeApp, setActiveApp] = useState('cartoon');

  return (
    <div className="min-h-screen bg-neutral-950 text-white">
      <nav className="p-4 bg-neutral-900">
        <button 
          className={`mr-4 ${activeApp === 'cartoon' ? 'text-blue-500' : 'text-white'}`}
          onClick={() => setActiveApp('cartoon')}
        >
          Cartoon Generator
        </button>
        <button 
          className={`${activeApp === 'audio' ? 'text-blue-500' : 'text-white'}`}
          onClick={() => setActiveApp('audio')}
        >
          News Audio Generator
        </button>
      </nav>
      {activeApp === 'cartoon' ? <NewsFunApp /> : <NewsAudioGen />}
    </div>
  );
};

export default App;

