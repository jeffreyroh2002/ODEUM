import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Header from "./components/Header"
import AudioPlayer from './components/AudioPlayer';
import Form from './components/Form';
import './Questionnaire.css';
import playIcon from './images/icons8-play-64.png'
import pauseIcon from './images/icons8-pause-64.png'
//import sample_audio from "./Audio/sample_audio.mp3"

export default function Questionnaire() {
    const location = useLocation();
    const navigate = useNavigate(); // Correctly moved to the top level of your component
    const searchParams = new URLSearchParams(location.search);
    const [audioFileId, setAudioFileId] = useState(searchParams.get('audio_file_id'));
    const testType = searchParams.get('test_type');

    const [audioFilePath, setAudioFilePath] = useState('');

    useEffect(() => {
        console.log("Fetching audio file for:", audioFileId); // Add this line to check if useEffect is triggered
        const queryParams = new URLSearchParams({ audio_file_id: audioFileId, test_type: testType }).toString();
        fetch(`/get_next_questions?${queryParams}`)
        .then(res => res.json())
        .then(data => {
            const path = `/static/audio_files/${data.audio_file_name}`;
            setAudioFilePath(path);
        })
        .catch(error => console.error('Error fetching audio file info:', error));
    }, [audioFileId, testType]);

    useEffect(() => {
        navigate(`/Questionnaire?audio_file_id=${audioFileId}&test_type=${testType}`, { replace: true });
    }, [audioFileId, testType, navigate]);

    const handleNextAudioFile = (nextAudioFileId) => {
        setAudioFileId(nextAudioFileId);
    };

    return (
        <div>
            <Header />
            <div>{audioFilePath}</div>
            <AudioPlayer 
                src={audioFilePath}
                playIconPath = {playIcon}
                pauseIconPath = {pauseIcon}
            />
            <Form audioFileId={audioFileId} testType={testType} onNextAudioFile={handleNextAudioFile} />
        </div>
    )
}