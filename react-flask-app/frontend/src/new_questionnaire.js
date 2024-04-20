import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Header from "./components/Header"
import AudioPlayer from './components/AudioPlayer';
import Form from './components/Form';
import AudioVisualizerSphere from './components/AudioVisualizerSphere'
import './Questionnaire.css';
import playIcon from './images/blob.png'
import pauseIcon from './images/dark_blob.png'
import axios from 'axios';
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

export default function Questionnaire() {
    const BASE_URL = process.env.REACT_APP_API_BASE_URL;
    
    const location = useLocation();
    const navigate = useNavigate(); // Correctly moved to the top level of your component
    const searchParams = new URLSearchParams(location.search);
    const testType = parseInt(searchParams.get('test_type'));
    const testId = parseInt(searchParams.get('test_id'));

    const numQuestionPerAudio = 4;
    const numAudios = 22;
    const numAdditionalQ = 0;
    const numQ = numAdditionalQ + numQuestionPerAudio * numAudios;

    const [isLoggedIn, setIsLoggedIn] = useState(true);
    const [questionIndex, setQuestionIndex] = useState(parseInt(searchParams.get('question_index')));
    const [questionType, setQuestionType] = useState('');
    const [audioId, setAudioId] = useState(1);
    const [audioName, setAudioName] = useState('');
    const [isLoading, setIsLoading] = useState(true);

    function handleLogout() { setIsLoggedIn(false); };

    useEffect(() => {
      navigate(`${BASE_URL}/Questionnaire?question_index=${questionIndex}&test_type=${testType}&test_id=${testId}`);
      setIsLoading(true);
      axios.get(`${BASE_URL}/get_question_metadata?question_index=${questionIndex}`)
           .then(response => { setQuestionType(response.data.question_type); 
                               setAudioId(response.data.audio_id); 
                               setAudioName(response.data.audio_filename); 
                               setIsLoading(false); })
           .catch((error) => { console.log("error getting question metadata", error); 
                               setIsLoading(false);});
    }, [questionIndex]);
    
    const goNextQ = () => {
        if (questionIndex !== numQ) setQuestionIndex(prev => prev + 1);
        else handleTestSubmit();
    };

    const goPrevQ = () => { setQuestionIndex(prev => prev - 1); };

    const MySwal = withReactContent(Swal);
    function handleTestSubmit() {
        MySwal.fire({
            title: "Do you want to submit the test in progress?",
            showConfirmButton: true,
            showDenyButton: false,
            showCancelButton: true,
            confirmButtonText: `Submit`
        }).then((result) => {
            if (result.isConfirmed) {
            navigate(`/TestCompleted?testId=${testId}`, { replace: true });
            };
        })
    }

    
    return (
        <div>
            <Header isLoggedIn={isLoggedIn} onLogout={handleLogout} />
            <div className="questionnaire-container">
              <div>{audioName}</div>
              {/*
              <AudioVisualizerSphere className="play--pause--button"
                  key={audioId}
                  src={audioName}
                  isPlaying={isPlaying}
                  togglePlayPause={handlePlayPause}
              />
              */}
              <AudioPlayer className="play--pause--button"
                  key={audioId}
                  src={audioName}
                  playIconPath = {playIcon}
                  pauseIconPath = {pauseIcon}
              />
              {isLoading? <div></div> :
              <Form 
                  testId={testId} 
                  questionIndex={questionIndex}
                  audioId={audioId}
                  onPrevQuestion={goPrevQ}
                  onNextQuestion={goNextQ}
                  numQ={numQ}
                  onQuit={handleQuit}
                  questionType={questionType}/> }
            </div>
        </div>
    )
};