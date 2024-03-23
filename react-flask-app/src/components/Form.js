import React, { useState, useEffect } from 'react';
import './Form.css';

export default function Form({ testId, questionIndex, onPrevQuestion, onNextQuestion }) {
  const [csrfToken, setCsrfToken] = useState('');
  const ANSWERS_PER_AUDIO = 4;

  // Fetch CSRF token on component mount if your Flask app has CSRF protection enabled
  useEffect(() => {
    fetch('/csrf-token').then(response => {
      return response.json();
    }).then(data => {
      setCsrfToken(data.csrf_token);
    });
  }, []);

  // submitting to the Flask backend
  function handleSelection(selection_type, type_rating) {
    // When a user selects an answer, post the answer to the backend
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
    .then(response => { if (!response.ok) { throw new Error('Network response was not ok'); } });
    onNextQuestion();
  }

  return (
    <div>
      <div className="rating--container">
        {/* Render questions based on currentQuestionIndex */}
        {questionIndex % ANSWERS_PER_AUDIO === 1 && (
          <div className="rating-group">
            <h4 className="rating--label">Rate the Song.</h4>
            <button className="rating--button" onClick={() => handleSelection('overall_rating', 3)}>could listen to it all day &#128293;</button>
            <button className="rating--button" onClick={() => handleSelection('overall_rating', 2)}>pretty decent</button>
            <button className="rating--button" onClick={() => handleSelection('overall_rating', 1)}>could get used to it</button>
            <button className="rating--button" onClick={() => handleSelection('overall_rating', -1)}>would not play it myself</button>
            <button className="rating--button" onClick={() => handleSelection('overall_rating', -2)}>eh...</button>
            <button className="rating--button" onClick={() => handleSelection('overall_rating', -3)}>hate it with a passion &#128556;</button>
          </div>
        )}

        {questionIndex % ANSWERS_PER_AUDIO === 2 && (
          <div className="rating-group">
            <h4 className="rating--label">How is the Genre?</h4>
            <button className="rating--button" onClick={() => handleSelection('genre_rating', 3)}>Fire</button>
            <button className="rating--button" onClick={() => handleSelection('genre_rating', 2)}>Decent</button>
            <button className="rating--button" onClick={() => handleSelection('genre_rating', 1)}>Not bad</button>
            <button className="rating--button" onClick={() => handleSelection('genre_rating', -1)}>Would not play it myself</button>
            <button className="rating--button" onClick={() => handleSelection('genre_rating', -2)}>eh...</button>
            <button className="rating--button" onClick={() => handleSelection('genre_rating', -3)}>Hate it</button>
            <button className="rating--button" onClick={() => handleSelection('genre_rating', 0)}>Not sure &#x1f937;</button>
          </div>
        )}

        {questionIndex % ANSWERS_PER_AUDIO === 3 && (
          <div className="rating-group">
            <h4 className="rating--label">Describe the vibe or feeling of this song.</h4>
            <button className="rating--button" onClick={() => handleSelection('mood_rating', 3)}>Fire</button>
            <button className="rating--button" onClick={() => handleSelection('mood_rating', 2)}>Decent</button>
            <button className="rating--button" onClick={() => handleSelection('mood_rating', 1)}>Not bad</button>
            <button className="rating--button" onClick={() => handleSelection('mood_rating', -1)}>Would not play it myself</button>
            <button className="rating--button" onClick={() => handleSelection('mood_rating', -2)}>eh...</button>
            <button className="rating--button" onClick={() => handleSelection('mood_rating', -3)}>Hate it </button>
            <button className="rating--button" onClick={() => handleSelection('mood_rating', 0)}>Not sure &#x1f937;</button>
          </div>
        )}

        {questionIndex % ANSWERS_PER_AUDIO === 0 && (
          <div className="rating-group">
            <h4 className="rating--label">Thoughts on the vocals?</h4>
            <button className="rating--button" onClick={() => handleSelection('vocal_timbre_rating', 3)}>Fire</button>
            <button className="rating--button" onClick={() => handleSelection('vocal_timbre_rating', 2)}>Decent</button>
            <button className="rating--button" onClick={() => handleSelection('vocal_timbre_rating', 1)}>Not bad</button>
            <button className="rating--button" onClick={() => handleSelection('vocal_timbre_rating', -1)}>Would not play it myself</button>
            <button className="rating--button" onClick={() => handleSelection('vocal_timbre_rating', -2)}>eh...</button>
            <button className="rating--button" onClick={() => handleSelection('vocal_timbre_rating', -3)}>Hate it</button>
            <button className="rating--button" onClick={() => handleSelection('vocal_timbre_rating', 0)}>Not sure &#x1f937;</button>
          </div>
        )}
      </div>
      
      <button className="prev--button" onClick={onPrevQuestion}>Previous Button</button>

      <button className="next--button" onClick={onNextQuestion}>Next Button</button>

    </div>
  );
}