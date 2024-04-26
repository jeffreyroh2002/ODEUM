import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import './streaming_AudioPlayer.css'

export default function Streaming_AudioPlayer({audioName, playIconPath, pauseIconPath}) {
    const [audioUrl, setAudioUrl] = useState('');
    const BASE_URL = process.env.REACT_APP_API_BASE_URL;

    // this component's src will be designated later
    const audioRef = useRef(new Audio());
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);

    useEffect(() => {
        axios.get(`${BASE_URL}/get_audio?audio_name=${audioName}`)
             .then(response => {
                setAudioUrl(response.data.url) ;
                audioRef.current.src = response.data.url;
                audioRef.current.pause();
                setIsPlaying(false);
                setCurrentTime(0);
                audioRef.current.load(); 
              })
             .catch(error => console.error('Error fetching audio URL:', error));        
    }, [])

    const togglePlayPause = () => {
        const prevValue = isPlaying;
        setIsPlaying(!prevValue);
        if (!prevValue) {
          audioRef.current.play();
        } else {
          audioRef.current.pause();
        }
    };

    return (
        <div className="audio--player--container">
            <button className="play--pause--button" onClick={togglePlayPause}>
                <img src={isPlaying ? pauseIconPath : playIconPath} alt={isPlaying ? 'Pause' : 'Play'} />
            </button>
        </div>
    );
};