import React, { useState, useEffect, useRef } from 'react';

const formatTime = (time) => {
  const minutes = Math.floor(time / 60);
  const seconds = Math.floor(time % 60);
  return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
};

const AudioPlayer = ({ src, playIconPath, pauseIconPath }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef(new Audio(src));

  const togglePlayPause = () => {
    const prevValue = isPlaying;
    setIsPlaying(!prevValue);
    if (!prevValue) {
      audioRef.current.play();
    } else {
      audioRef.current.pause();
    }
  };

  const onTimeSliderChange = (e) => {
    const time = e.target.value;
    setCurrentTime(time);
    audioRef.current.currentTime = time;
  };

  useEffect(() => {
    const audio = audioRef.current;
    audio.addEventListener('loadedmetadata', () => {
      setDuration(audio.duration);
    });

    audio.addEventListener('timeupdate', () => {
      setCurrentTime(audio.currentTime);
    });

    return () => {
      audio.removeEventListener('loadedmetadata', () => {
        setDuration(audio.duration);
      });
      audio.removeEventListener('timeupdate', () => {
        setCurrentTime(audio.currentTime);
      });
    };
  }, [audioRef]);

  useEffect(() => {
    setIsPlaying(!audioRef.current.paused);
  }, [currentTime]);

  return (
    <div className="audio--player--container">
      <div className="audio--timeline--container">
        <span>{formatTime(currentTime)}</span>
        <input
          type="range"
          value={currentTime}
          step="1"
          min="0"
          max={duration || 0}
          className="time-slider"
          onChange={onTimeSliderChange}
          style={{ flexGrow: 1 }}
        />
        <span>{formatTime(duration)}</span>
      </div>
      <button className="play--pause--button" onClick={togglePlayPause}>
        <img src={isPlaying ? pauseIconPath : playIconPath} alt={isPlaying ? 'Pause' : 'Play'} />
      </button>
    </div>
  );
};

export default AudioPlayer;