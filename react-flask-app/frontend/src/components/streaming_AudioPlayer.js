import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import './streaming_AudioPlayer.css'

export default function Streaming_AudioPlayer({audioName, playIconPath, pauseIconPath}) {
    const BASE_URL = process.env.REACT_APP_API_BASE_URL;

    // this component's src will be designated later
    const audioRef = useRef(new Audio());
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [loadingAudio, setLoadingAudio] = useState(true);

    useEffect(() => {
        setLoadingAudio(true);
        axios.get(`${BASE_URL}/stream_audio?audio_name=${audioName}`)
             .then(response => {
                audioRef.current.src = response.data.url;
                audioRef.current.pause();
                setIsPlaying(false);
                setCurrentTime(0);
                audioRef.current.load(); 
              })
             .catch(error => console.error('Error fetching audio URL:', error))
             .then(setLoadingAudio(false));      
    }, [audioName])

    const togglePlayPause = () => {
        if (!loadingAudio) {
            setIsPlaying(prev => !prev); 
            if (!isPlaying) {
                audioRef.current.play();
            } else {
                audioRef.current.pause();
            }
        }
    };

    return (
        <div className="audio--player--container">
            <button className="play--pause--button" onClick={togglePlayPause} disabled={loadingAudio}>
                <img src={isPlaying ? pauseIconPath : playIconPath} alt={isPlaying ? 'Pause' : 'Play'} />
            </button>
        </div>
    );
};