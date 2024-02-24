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
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const audioFileId = searchParams.get('audio_file_id');
    const testType = searchParams.get('test_type');

    const [audioFilePath, setAudioFilePath] = useState('');

    useEffect(() => {
        const queryParams = new URLSearchParams({ audio_file_id: audioFileId, test_type: testType }).toString();
        fetch(`/get_next_questions?${queryParams}`)
        .then(res => res.json())
        .then(data => {
            // Assuming your server's static directory is structured as '/static/audio_files/'
            // and data.audio_file_name is the filename of the next audio file
            const path = `/static/audio_files/${data.audio_file_name}`;
            setAudioFilePath(path);
        })
        .catch(error => console.error('Error fetching audio file info:', error));
    }, [audioFileId, testType]);

    return (
        <div>
            <Header />
            <div>{audioFilePath}</div>
            <AudioPlayer 
                src={audioFilePath}
                playIconPath = {playIcon}
                pauseIconPath = {pauseIcon}
            />
            <Form audioFileId={audioFileId} testType={testType} />
        </div>
    )
}