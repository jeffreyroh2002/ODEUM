import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Questionnaire.css';
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import Header from "./components/Header"
import Streaming_AudioPlayer from './components/streaming_AudioPlayer';
import playIcon from './images/blob.png'
import pauseIcon from './images/dark_blob.png'

export default function Questionnaire() {
    const BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const [isLoggedIn, setIsLoggedIn] = useState(true);
    function handleLogout() { setIsLoggedIn(false); };

    const navigate = useNavigate();
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const [testId, setTestId] = useState(parseInt(searchParams.get('test_id')));

    const [csrfToken, setCsrfToken] = useState('');    

    const [questionIndex, setQuestionIndex] = useState(0);
    const [audioId, setAudioId] = useState(1);
    const [audioName, setAudioName] = useState('');
    const [savedRating, setSavedRating] = useState(null);    

    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
      fetch(`${BASE_URL}/csrf-token`).then(response => {
        return response.json();
      }).then(data => { setCsrfToken(data.csrf_token); }); 
      axios.get(`${BASE_URL}/get_question_metadata?audio_id=${audioId}`)
           .then(response => { setAudioName(response.data.audio_filename); setIsLoading(false); });
    }, []);


    function handleButtonClick(rating) {
        setIsLoading(true);
        //check if a button is already clicked
        const clickedButton = document.querySelector('.yellow--background');

        //the case when the same button is clickced
        if (clickedButton && clickedButton.id === String(rating)) {
          setSavedRating(null);
          setIsLoading(false);
        }

        //the case when another button is clicked
        else { 
          console.log("clicked rating", rating);
          //first, submit the user answer data
          submitAnswer(rating, questionIndex, audioId)
            //it must be ensured that the next audio is gotten 'after' the answer is submitted 
          .then(() => getNextAudioData())
          .catch(error => console.error("Failed to submit answer and get next data:", error))
          .then(setIsLoading(false));
        }
    };

    function submitAnswer(rating, questionIndex, audioId) {
        return axios.post(`${BASE_URL}/submit_answer`, {
            rating: rating,
            audio_id: audioId,
            question_index: questionIndex,
            test_id: testId
            }, {
            headers: {
              'X-CSRF-Token': csrfToken // Replace `csrfToken` with the actual token
            }
        });
    };
    
    const MySwal = withReactContent(Swal);

    function getNextAudioData() {
      return axios.get(`${BASE_URL}/get_next_audio_id?test_id=${testId}&question_index=${questionIndex}`)
                  .then(response => {
                      console.log("response: ", response)
                      const nextAudioId = response.data.next_audio_id;
                      if (nextAudioId) {
                        setQuestionIndex(prev => prev + 1);
                        setAudioId(nextAudioId);
                        setAudioName(response.data.next_audio_name);
                        loadRating(nextAudioId);
                      }  
                      else {
                        MySwal.fire({
                            title: "Do you want to submit the test in progress?",
                            showConfirmButton: true,
                            showDenyButton: false,
                            showCancelButton: true,
                            confirmButtonText: `Submit`
                        })
                        .then((result) => {
                          if (result.isConfirmed) { navigate(`/TestCompleted?testId=${testId}`, { replace: true }); };
                             })                    
                      }
                  })
      };

    function loadRating(audioId) {
      axios.get(`${BASE_URL}/get_rating?audio_id=${audioId}&test_id=${testId}`)
      .then(response => { setSavedRating(response.data.rating); })
      .catch(error => console.log(error));   
    };

    useEffect(() => {
      const buttons = document.querySelectorAll('.rating--button');
      buttons.forEach(button => { button.classList.remove('yellow--background') });
      if (savedRating) {
        const button = document.getElementById(String(savedRating));
        button.classList.add('yellow--background');
      }
    }, [savedRating]);

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
          navigate('/');
        };
      })
    };

    function handleNextClick() {
      if (savedRating === null) {
        MySwal.fire({
          icon: "error",
          title: "This question is required!",
        });
      }
      else {
        console.log("isLoading in questionIndex before submitting", questionIndex, isLoading);
        submitAnswer(savedRating, questionIndex, audioId)
        .then(() => getNextAudioData())
        .catch(error => console.error("Failed to submit answer and get next data:", error))
        .then(setIsLoading(false));
      }
    };
    
    function handlePrevClick() {
      submitAnswer(savedRating, questionIndex, audioId)
      .then(() => getPrevAudioData())
      .catch(error => console.error("Failed to submit answer and get prev data:", error))
      .then(setIsLoading(false));
    }

    function getPrevAudioData() {
      setIsLoading(true);
      axios.get(`${BASE_URL}/get_prev_audio_id?test_id=${testId}&question_index=${questionIndex}`)
           .then(response => {
              setQuestionIndex(prev => prev - 1);
              setAudioId(response.data.prev_audio_id);
              setAudioName(response.data.prev_audio_name);
              loadRating(response.data.prev_audio_id);
            })
           .then(setIsLoading(false));   
    };

    return (
        <div>
            <Header isLoggedIn={isLoggedIn} onLogout={handleLogout} />
            <div className="questionnaire-container">
              <div>{audioName}</div>
              {!isLoading && 
              <Streaming_AudioPlayer 
                  audioName={audioName}
                  playIconPath = {playIcon}
                  pauseIconPath = {pauseIcon} />}
              <div className="rating-group">
                <h4 className="rating--label">Rate the Song.</h4>
                <button className="rating--button" id="3" onClick={() => handleButtonClick(3)} disabled={isLoading}>
                could listen to it all day &#128293;</button>
                <button className="rating--button" id="2" onClick={() => handleButtonClick(2)} disabled={isLoading}>
                pretty decent</button>
                <button className="rating--button" id="1" onClick={() => handleButtonClick(1)} disabled={isLoading}>
                could get used to it</button>
                <button className="rating--button" id="-1" onClick={() => handleButtonClick(-1)} disabled={isLoading}>
                would not play it myself</button>
                <button className="rating--button" id="-2" onClick={() => handleButtonClick(-2)} disabled={isLoading}>
                I don't like it ...</button>
                <button className="rating--button" id="-3" onClick={() => handleButtonClick(-3)} disabled={isLoading}>
                hate it with a passion &#128556;</button>
              </div>

              {questionIndex === 0 ? 
              <button className="quit--button" onClick={handleQuit} disabled={isLoading}>Quit Test</button> :
              <button className="prev--button" onClick={handlePrevClick} disabled={isLoading}>Previous Button</button>
              }

              <button className="next--button" onClick={handleNextClick} disabled={isLoading}>Next Button</button>
              </div>
        </div>
    ); 
};