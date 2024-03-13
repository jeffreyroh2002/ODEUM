import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Header from "./components/Header"
import new_audioplayer from './components/new_audioplayer';
import Form from './components/Form';
import './Questionnaire.css';
import playIcon from './images/blob.png'
import pauseIcon from './images/icons8-pause-64.png'
//import sample_audio from "./Audio/sample_audio.mp3"

export default function Questionnaire() {
    const location = useLocation();
    const navigate = useNavigate(); // Correctly moved to the top level of your component
    const searchParams = new URLSearchParams(location.search);
    const [audioFileId, setAudioFileId] = useState(searchParams.get('audio_file_id'));
    const testType = searchParams.get('test_type');
    const testId = searchParams.get('test_id');

    const [audioFilePath, setAudioFilePath] = useState('');

    useEffect(() => {
        console.log("testID in Q:", testId);
        const queryParams = new URLSearchParams({ audio_file_id: audioFileId, test_type: testType, test_id: testId }).toString();
        fetch(`/get_next_questions?${queryParams}`)
        .then(res => res.json())
        .then(data => {
            const path = `/static/audio_files/${data.audio_file_name}`;
            setAudioFilePath(path);
        })
        .catch(error => console.error('Error fetching audio file info:', error));
    }, [audioFileId, testType]);

    useEffect(() => {
        navigate(`/Questionnaire?audio_file_id=${audioFileId}&test_type=${testType}&test_id=${testId}`, { replace: true });
    }, [audioFileId, testType, navigate]);

    const handleAudioFile = (AudioFileId) => {
        console.log('Next audio file id:', AudioFileId);
        setAudioFileId(AudioFileId);
    };

    return (
        <div>
            <Header />
            <div className="questionnaire-container">
                <div>Song {audioFileId}</div>
                <new_audioplayer 
                    key={audioFileId}
                    src={audioFilePath}
                    playIconPath = {playIcon}
                    pauseIconPath = {pauseIcon}
                />
                <Form 
                    audioFileId={audioFileId} 
                    testId={testId} 
                    onAudioFile={handleAudioFile}/>
            </div>
        </div>
    )
}