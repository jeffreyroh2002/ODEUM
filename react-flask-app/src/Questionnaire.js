import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Header from "./components/Header"
import AudioPlayer from './components/AudioPlayer';
import Form from './components/Form';
import AudioVisualizerSphere from './components/AudioVisualizerSphere'
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
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false); 

    useEffect(() => {
        console.log('Audio file path:', audioFilePath);
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
        // Code that uses the updated audioFilePath 
        console.log('Updated audio file path:', audioFilePath);  
    }, [audioFilePath]); // Add a useEffect that depends on audioFilePath
    
    useEffect(() => {
        navigate(`/Questionnaire?audio_file_id=${audioFileId}&test_type=${testType}&test_id=${testId}`, { replace: true });
    }, [audioFileId, testType, testId, navigate]);

    const handleNextQuestion = () => {
        setCurrentQuestionIndex(prevIndex => prevIndex + 1);
    };

    const handlePrevQuestion = () => {
        setCurrentQuestionIndex(prevIndex => prevIndex - 1);
    };

    const setQuestion = () => {
        setCurrentQuestionIndex(prevIndex => prevIndex);
    };

    const handleAudioFile = (audioFileId) => {
        console.log('Next audio file id:', audioFileId);
        setAudioFileId(audioFileId);
        setCurrentQuestionIndex(0); // Reset current question index when changing audio file
    };

    const handlePlayPause = () => {
        setIsPlaying(!isPlaying);
    }

    return (
        <div>
            <Header />
            <div className="questionnaire-container">
                <div>{audioFilePath}</div>
                {/*
                <AudioVisualizerSphere className="play--pause--button"
                    key={audioFileId}
                    src={audioFilePath}
                    isPlaying={isPlaying}
                    togglePlayPause={handlePlayPause}
                />
                */}
                <AudioPlayer className="play--pause--button"
                    key={audioFileId}
                    src={audioFilePath}
                    playIconPath = {playIcon}
                    pauseIconPath = {pauseIcon}
                />
                <Form 
                    audioFileId={audioFileId} 
                    testId={testId} 
                    currentQuestionIndex={currentQuestionIndex}
                    setQuestion = {setQuestion}
                    onPrevQuestion={handlePrevQuestion}
                    onNextQuestion={handleNextQuestion}
                    onAudioFile={handleAudioFile}/>
            </div>
        </div>
    )
}