import React, { useState, useEffect } from 'react';
import Header from "./components/Header"
import { Link } from 'react-router-dom';
import './Presurvey.css';
import axios from 'axios';

function Questionnaire() {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [csrfToken, setCsrfToken] = useState('');

  useEffect(() => {
    axios.get('/csrf-token').then(response => {
      setCsrfToken(response.data.csrf_token);
    });
  }, []);

  useEffect(() => {
    // Fetch questions from the backend at the start
    axios.get('/get_presurvey_questions').then(response => {
      setQuestions(response.data);
    });
  }, []);

  const handleAnswerSubmit = answer => {
    // Send answer to backend
    axios.post('/process_presurvey_questions', { 
        questionId: questions[currentQuestionIndex].id, 
        answer 
    }, {
        headers: {
            'X-CSRF-Token': csrfToken // Replace `csrfToken` with the actual token
          }
    }).then(response => {
        // Optionally handle response, e.g., for validation
      }).catch(error => {
        console.error('Error posting data:', error);
      });

    // Save answer locally (optional, depends on needs)
    setAnswers(prevAnswers => [...prevAnswers, {questionId: questions[currentQuestionIndex].id, answer}]);

    // Move to next question
    setCurrentQuestionIndex(prevIndex => prevIndex + 1);
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
            <div className="question--group">
                <button className="question--button" key={index} onClick={() => handleAnswerSubmit(answer)}>
                    {answer}
                </button>
            </div>
            ))}
        </div>
    </div>
  );
}

export default Questionnaire;
