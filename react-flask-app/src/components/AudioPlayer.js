import React, { useState, useEffect, useRef } from 'react';

const AudioPlayer = ({ src, playIconPath, pauseIconPath }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const audioRef = useRef(new Audio(src));

  useEffect(() => {
    console.log('Audio file path:', src);
  }, [src]);


  useEffect(() => {
    audioRef.current.src = src;
    audioRef.current.pause();
    setIsPlaying(false);
    setCurrentTime(0);
    audioRef.current.load();
  }, [src]);
  
  const togglePlayPause = () => {
    const prevValue = isPlaying;
    setIsPlaying(!prevValue);
    if (!prevValue) {
      audioRef.current.play();
    } else {
      audioRef.current.pause();
    }
  };

  useEffect(() => {
    setIsPlaying(!audioRef.current.paused);
  }, [currentTime]);

  return (
    <div className="audio--player--container">
      <button className="play--pause--button" onClick={togglePlayPause}>
        <img src={isPlaying ? pauseIconPath : playIconPath} alt={isPlaying ? 'Pause' : 'Play'} />
      </button>
    </div>
  );
};

export default AudioPlayer;