import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Header from "./components/Header"
import AudioPlayer from './components/AudioPlayer';
import Form from './components/Form';
import './Questionnaire.css';
import playIcon from './images/blob.png'
import pauseIcon from './images/dark_blob.png'
//import sample_audio from "./Audio/sample_audio.mp3"

export default function Questionnaire() {
    const location = useLocation();
    const navigate = useNavigate(); // Correctly moved to the top level of your component
    const searchParams = new URLSearchParams(location.search);
    const [audioFileId, setAudioFileId] = useState(searchParams.get('audio_file_id'));
    const testType = searchParams.get('test_type');
    const testId = searchParams.get('test_id');

    const [audioFilePath, setAudioFilePath] = useState('');
    const [questionIndex, setQuestionIndex] = useState(1);

    useEffect(() => {
        const queryParams = new URLSearchParams({ audio_file_id: audioFileId, test_type: testType, test_id: testId }).toString();
        fetch(`/get_next_questions?${queryParams}`)
        .then(res => res.json())
        .then(data => {
            const path = `/static/audio_files/${data.audio_file_name}`;
            setAudioFilePath(path);
        })
        .catch(error => console.error('Error fetching audio file info:', error));
    }, [audioFileId, testType, testId]);

    useEffect(() => {
        navigate(`/Questionnaire?audio_file_id=${audioFileId}&test_type=${testType}&test_id=${testId}`, { replace: true });
    }, [audioFileId, testType, testId, navigate]);

    const handleNextQuestion = () => {
        setQuestionIndex(prevIndex => prevIndex + 1);
    };

    const handlePrevQuestion = () => {
        setQuestionIndex(prevIndex => prevIndex - 1);
    };

    return (
        <div>
            <Header />
            <div className="questionnaire-container">
                <div>{audioFilePath}</div>
                <AudioPlayer className="play--pause--button"
                    key={audioFileId}
                    src={audioFilePath}
                    playIconPath = {playIcon}
                    pauseIconPath = {pauseIcon}
                />
                <Form 
                    testId={testId} 
                    questionIndex={questionIndex}
                    onPrevQuestion={handlePrevQuestion}
                    onNextQuestion={handleNextQuestion}/>
            </div>
        </div>
    )
}