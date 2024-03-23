import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Form.css';

export default function Form({ testId, questionIndex, onPrevQuestion, onNextQuestion }) {
  const navigate = useNavigate();
  const [csrfToken, setCsrfToken] = useState('');
  const [selection, setSelection] = useState(0);
  const NUM_AUDIOS = 3;
  const ANSWERS_PER_AUDIO = 4;
  const EXTRA_ANSWERS = 0;
  const NUM_ANSWERS = NUM_AUDIOS * ANSWERS_PER_AUDIO + EXTRA_ANSWERS;

  // Fetch CSRF token on component mount if your Flask app has CSRF protection enabled
  useEffect(() => {
    fetch('/csrf-token').then(response => {
      return response.json();
    }).then(data => {
      setCsrfToken(data.csrf_token);
    });
  }, []);

  function handlePrevButton() {
    if (questionIndex !== 0) {
      onPrevQuestion();
    } 
  };
  
  function handleNextButton() {
    onNextQuestion();
  }

  // submitting to the Flask backend
  function handleSelection(selection_type, type_rating) {
    console.log(testId, questionIndex, selection_type, type_rating);
    fetch('/submit_answer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        test_id: testId,
        question_index: questionIndex,
        type: selection_type,
        rating: type_rating 
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
    });

    if (questionIndex === NUM_ANSWERS) {
      navigate(`/TestCompleted?testId=${testId}`, { replace: true });
    } 
    else { onNextQuestion() };
  }


  function handleOverallButton(rating){
    setSelection(rating);
    handleSelection('overall_rating', rating);
  }
  function handleGenreButton(rating){
    setSelection(rating);
    handleSelection('genre_rating', rating)
  }
  function handleMoodButton(rating){
    setSelection(rating);
    handleSelection('mood_rating', rating)
  }
  function handleVocalButton(rating){
    setSelection(rating);
    handleSelection('vocal_timbre_rating', rating)
  }

  return (
    <div>
      <div className="rating--container">
        {/* Render questions based on currentQuestionIndex */}
        {questionIndex % 4 === 1 && (
          <div className="rating-group">
            <h4 className="rating--label">Rate the Song.</h4>
            <button className="rating--button" onClick={() => handleOverallButton(3)}>could listen to it all day &#128293;</button>
            <button className="rating--button" onClick={() => handleOverallButton(2)}>pretty decent</button>
            <button className="rating--button" onClick={() => handleOverallButton(1)}>could get used to it</button>
            <button className="rating--button" onClick={() => handleOverallButton(-1)}>would not play it myself</button>
            <button className="rating--button" onClick={() => handleOverallButton(-2)}>eh...</button>
            <button className="rating--button" onClick={() => handleOverallButton(-3)}>hate it with a passion &#128556;</button>
          </div>
        )}

        {questionIndex % 4 === 2 && (
          <div className="rating-group">
            <h4 className="rating--label">How is the Genre?</h4>
            <button className="rating--button" onClick={() => handleGenreButton(3)}>Fire</button>
            <button className="rating--button" onClick={() => handleGenreButton(2)}>Decent</button>
            <button className="rating--button" onClick={() => handleGenreButton(1)}>Not bad</button>
            <button className="rating--button" onClick={() => handleGenreButton(-1)}>Would not play it myself</button>
            <button className="rating--button" onClick={() => handleGenreButton(-2)}>eh...</button>
            <button className="rating--button" onClick={() => handleGenreButton(-3)}>Hate it</button>
            <button className="rating--button" onClick={() => handleGenreButton(0)}>Not sure &#x1f937;</button>
          </div>
        )}

        {questionIndex % 4 === 3 && (
          <div className="rating-group">
            <h4 className="rating--label">Describe the vibe or feeling of this song.</h4>
            <button className="rating--button" onClick={() => handleMoodButton(3)}>Fire</button>
            <button className="rating--button" onClick={() => handleMoodButton(2)}>Decent</button>
            <button className="rating--button" onClick={() => handleMoodButton(1)}>Not bad</button>
            <button className="rating--button" onClick={() => handleMoodButton(-1)}>Would not play it myself</button>
            <button className="rating--button" onClick={() => handleMoodButton(-2)}>eh...</button>
            <button className="rating--button" onClick={() => handleMoodButton(-3)}>Hate it </button>
            <button className="rating--button" onClick={() => handleMoodButton(0)}>Not sure &#x1f937;</button>
          </div>
        )}

        {questionIndex % 4 === 0 && (
          <div className="rating-group">
            <h4 className="rating--label">Thoughts on the vocals?</h4>
            <button className="rating--button" onClick={() => handleVocalButton(3)}>Fire</button>
            <button className="rating--button" onClick={() => handleVocalButton(2)}>Decent</button>
            <button className="rating--button" onClick={() => handleVocalButton(1)}>Not bad</button>
            <button className="rating--button" onClick={() => handleVocalButton(-1)}>Would not play it myself</button>
            <button className="rating--button" onClick={() => handleVocalButton(-2)}>eh...</button>
            <button className="rating--button" onClick={() => handleVocalButton(-3)}>Hate it</button>
            <button className="rating--button" onClick={() => handleVocalButton(0)}>Not sure &#x1f937;</button>
          </div>
        )}
      </div>
      
      <button className="prev--button" onClick={handlePrevButton}>
        Previous Button
      </button>

      <button className="next--button" onClick={handleNextButton}>
        Next Button
      </button>

    </div>
  );
}