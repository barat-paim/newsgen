import React, { useState, useEffect } from 'react';

function LoadingComponent({ loadComplete }) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let interval = setInterval(() => {
      setProgress((oldProgress) => {
        if (oldProgress < 100) {
          return oldProgress + 3.3;
        }
        clearInterval(interval);
        loadComplete();
        return 100;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [loadComplete]);

  return (
    <div className="loading-background">
      <p className="text-white text-2xl font-bold">Loading {Math.round(progress)}%</p>
    </div>
  );
}

export default LoadingComponent;