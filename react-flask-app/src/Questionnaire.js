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
    const audioFiles = [
        `static/audio_files/Aimyon.wav_1.wav`,
        `static/audio_files/FKJ_something.wav_2.wav`,
        `static/audio_files/KendrickLamar.wav_3.wav`,
    ]

    const [audioFileId, setAudioFileId] = useState(1);
    const currentAudioFileId = parseInt(searchParams.get('audio_file_id'));
    const testType = parseInt(searchParams.get('test_type'));
    const testId = parseInt(searchParams.get('test_id'));

    const [questionIndex, setQuestionIndex] = useState(4 * currentAudioFileId - 3);
    const [audioFilePath, setAudioFilePath] = useState(audioFiles[currentAudioFileId - 1]);


    useEffect(() => {
        if (Math.ceil(questionIndex / 4) !== audioFileId) {
            setAudioFileId(Math.ceil(questionIndex / 4))
        }
    }, [questionIndex])

    useEffect(() => {
        setAudioFilePath(audioFiles[audioFileId - 1])
    }, [audioFileId])

    useEffect(() => {
        if (currentAudioFileId !== audioFileId) {
            navigate(`/Questionnaire?audio_file_id=${audioFileId}&test_type=${testType}&test_id=${testId}`)
        }
    }, [audioFilePath])

    const handleNextQuestion = () => {
        if (questionIndex === 12) navigate(`/TestCompleted?testId=${testId}`, { replace: true });
        else setQuestionIndex(prevIndex => prevIndex + 1);
    };

    const handlePrevQuestion = () => {
        if (questionIndex !== 1) setQuestionIndex(prevIndex => prevIndex - 1);
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