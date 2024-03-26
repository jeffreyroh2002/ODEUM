import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Header from "./components/Header"
import AudioPlayer from './components/AudioPlayer';
import Form from './components/Form';
import './Questionnaire.css';
import playIcon from './images/blob.png'
import pauseIcon from './images/dark_blob.png'
import axios from 'axios';
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

export default function Questionnaire() {
    const location = useLocation();
    const navigate = useNavigate(); // Correctly moved to the top level of your component
    const searchParams = new URLSearchParams(location.search);

    const [audioFileId, setAudioFileId] = useState(searchParams.get('audio_file_id'));
    const [audioFilePath, setAudioFilePath] = useState('');
    const currentAudioFileId = parseInt(searchParams.get('audio_file_id'));
    const testType = parseInt(searchParams.get('test_type'));
    const testId = parseInt(searchParams.get('test_id'));
    const questionsNum = 4;
    const [questionIndex, setQuestionIndex] = useState(questionsNum * (audioFileId - 1) + 1);
    const [audiosNum, setAudiosNum] = useState(2);

    const MySwal = withReactContent(Swal)

    //getting the number of audio files
    useEffect(() => {
        axios.get('/get_audio_num')
             .then(response => { setAudiosNum(parseInt(response.data.num_audio)) });
    }, [])

    useEffect(() => {
        if (Math.ceil(questionIndex / questionsNum) !== audioFileId) {
            setAudioFileId(Math.ceil(questionIndex / questionsNum))
        }
    }, [questionIndex, audiosNum])

    useEffect(() => {
        axios.get(`/get_audio_filename?audio_id=${audioFileId}`)
             .then((response) => { setAudioFilePath(response.data.audio_filename); })
    }, [audioFileId])

    useEffect(() => {
        if (currentAudioFileId !== audioFileId) {
            navigate(`/Questionnaire?audio_file_id=${audioFileId}&test_type=${testType}&test_id=${testId}`)
        }
    }, [audioFilePath])
    
    const handleNextButton = () => { 
        if (questionIndex !== audiosNum * questionsNum) setQuestionIndex(prev => prev + 1);
        else handleTestSubmit();
    };
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
    const handlePrevButton = () => { setQuestionIndex(prevIndex => prevIndex - 1); };
    
    function handleQuit() {
        MySwal.fire({
          title: "Do you want to quit the test in progress?",
          showConfirmButton: false,
          showDenyButton: true,
          showCancelButton: true,
          denyButtonText: `Quit`
        }).then((result) => {
          if (result.isDenied) {
            MySwal.fire({
              title: "Navigating to home...",
              timer: 500,
              timerProgressBar: false,
              didOpen: () => {
                Swal.showLoading();
              }
            });
          };
          navigate('/');
        })
      }
    

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
                    onPrevButton={handlePrevButton}
                    onNextButton={handleNextButton}
                    audiosNum={audiosNum}
                    questionsNum={questionsNum}
                    onQuit={handleQuit}
                    onTestSubmit={handleTestSubmit}/>
            </div>
        </div>
    )
}