import React, { useState, useEffect } from 'react';
import Header from "./components/Header"
import { Link } from 'react-router-dom';
import './Presurvey.css';
import axios from 'axios';

function Questionnaire() {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState([]);

  useEffect(() => {
    // Fetch questions from the backend at the start
    axios.get('/get_presurvey_questions').then(response => {
      setQuestions(response.data);
    });
  }, []);

  const handleAnswerSubmit = answer => {
    // Send answer to backend
    axios.post('/process_presurvey_questions', { questionId: questions[currentQuestionIndex].id, answer })
      .then(response => {
        // Optionally handle response, e.g., for validation
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
      <h2>{currentQuestion.text}</h2>
      {/* Render buttons based on the current question's answers */}
      <div>
        {currentQuestion.answers.map((answer, index) => (
          <button key={index} onClick={() => handleAnswerSubmit(answer)}>
            {answer}
          </button>
        ))}
      </div>
    </div>
  );
}

export default Questionnaire;
