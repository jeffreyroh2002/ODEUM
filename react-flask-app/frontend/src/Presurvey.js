import React, { useState, useEffect } from 'react';
import Header from "./components/Header"
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import './Presurvey.css';
import axios from 'axios';

function Questionnaire() {
  const BASE_URL = process.env.REACT_APP_API_BASE_URL;

  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [csrfToken, setCsrfToken] = useState('');

  useEffect(() => {
    axios.get(`${BASE_URL}/csrf-token`).then(response => {
      setCsrfToken(response.data.csrf_token);
    });
  }, []);

  useEffect(() => {
    // Fetch questions from the backend at the start
    axios.get(`${BASE_URL}/get_presurvey_questions`).then(response => {
      setQuestions(response.data);
    });
  }, []);

  
  const handleAnswerSelection = answer => {
    if (questions[currentQuestionIndex].allow_multiple) {
      if (selectedAnswers.includes(answer)) {
        setSelectedAnswers(selectedAnswers.filter(a => a !== answer));
      } else {
        setSelectedAnswers([...selectedAnswers, answer]);
      }
    } else {
      setSelectedAnswers([answer]);
    }
  };

  const handleAnswerSubmit = () => {
    // Prepare the data to send all answers at once
    const payload = {
      questionId: questions[currentQuestionIndex].id,
      answers: selectedAnswers
    };
  
    axios.post(`${BASE_URL}/process_presurvey_questions`, payload, {
      headers: {
        'X-CSRF-Token': csrfToken
      }
    }).then(response => {
        // Optionally handle response, such as confirming submission
        console.log('Answers submitted successfully:', response.data);
    }).catch(error => {
        console.error('Error posting data:', error);
        // Optionally add retry logic or user notification here
    });
  
    // Save answers locally
    setAnswers(prevAnswers => [...prevAnswers, ...selectedAnswers.map(answer => ({ questionId: questions[currentQuestionIndex].id, answer }))]);
  
    // Move to next question if not the last one
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prevIndex => prevIndex + 1);
      // Reset selected answers for the next question
      setSelectedAnswers([]);
    } else {
      console.log('Completed all questions.');
      navigate(`/ArtistSelector`)
    }
  };

  if (questions.length === 0) return <div>Loading...</div>;
  if (currentQuestionIndex >= questions.length) return <div>Questionnaire completed!</div>;

  const currentQuestion = questions[currentQuestionIndex];

  return (
    <div>
        <Header />
        <h2 className="question--label">{currentQuestion.text}</h2>
        {/* Render buttons based on the current question's answers */}
        <div>
            {currentQuestion.answers.map((answer, index) => (
            <div className="question--group" key={index}>
                <button className={`question--button ${selectedAnswers.includes(answer) ? 'selected' : ''}`} onClick={() => handleAnswerSelection(answer)}>
                    {answer}
                </button>
            </div>
            ))}
        </div>
        <button className="submit--button" onClick={handleAnswerSubmit}>Next</button>
    </div>
  );
}

export default Questionnaire;