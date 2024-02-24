import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Header from "./components/Header"
import AudioPlayer from './components/AudioPlayer';
import Form from './components/Form';
import './Questionnaire.css';
import playIcon from './images/icons8-play-64.png'
import pauseIcon from './images/icons8-pause-64.png'
//import sample_audio from "./Audio/sample_audio.mp3"

export default function Questionnaire() {
    // Get the location object using useLocation hook
    const location = useLocation();

    // Extract audio_file_id from location.search
    const searchParams = new URLSearchParams(location.search);
    const audioFileId = searchParams.get('audio_file_id');
    const testType = searchParams.get('test_type');

    const [audioFilePath, setAudioFilePath] = useState('');

    useEffect(() => {
        // Construct query parameters string
        const queryParams = new URLSearchParams({ audio_file_id: audioFileId, test_type: testType }).toString();

        fetch(`/get_next_questions?${queryParams}`)
        .then(res => res.json())
        .then(data => {
            setAudioFilePath(`./Audio/${data.audio_file}`);
        })
        .catch(error => console.error('Error fetching song:', error));

    }, [audioFileId, testType]);

    return (
        <div>
            <Header />
            <AudioPlayer 
                src={audioFilePath}
                playIconPath = {playIcon}
                pauseIconPath = {pauseIcon}
            />
            <Form audioFileId={audioFileId} testType={testType} />
        </div>
    )
}