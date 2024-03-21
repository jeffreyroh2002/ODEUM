import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Form.css';

export default function Form({ testId, questionIndex, onPrevQuestion, onNextQuestion }) {
  const navigate = useNavigate();
  const [csrfToken, setCsrfToken] = useState('');
  const [selection, setSelection] = useState(0);
  const [type, setType] = useState('');
  const NUM_AUDIOS = 3;
  const ANSWERS_PER_AUDIO = 4;
  const EXTRA_ANSWERS = 0;
  const NUM_ANSWERS = NUM_AUDIOS * ANSWERS_PER_AUDIO + EXTRA_ANSWERS;

  const audioFileId = Math.ceil(questionIndex / 4);

  // Fetch CSRF token on component mount if your Flask app has CSRF protection enabled
  useEffect(() => {
    fetch('/csrf-token').then(response => {
      return response.json();
    }).then(data => {
      setCsrfToken(data.csrf_token);
    });
  }, []);

  function handlePrevButton() {
    if (questionIndex === 0) {
      
    }
    else {

    }
  };
  
  // submitting to the Flask backend
  function handleNextButton(type, rating) {
    if (questionIndex === NUM_ANSWERS) {
      navigate(`TestCompleted?testId=${testId}`, { replace: true });
    } else {
      console.log("selection:", rating); // 변경된 부분: rating을 직접 사용
      fetch('/submit_answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken, // Assuming CSRF protection is enabled
        },
        body: JSON.stringify({
          test_id: testId,
          audio_id: audioFileId,
          type: type,
          rating: rating // 변경된 부분: rating을 직접 사용
        })
      })
      .then(response => {
        console.log("here: ", rating); // 변경된 부분: rating을 직접 사용
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        onNextQuestion();
      });
    }
  }

  function handleOverallButton(rating){
    setSelection(rating);
    handleNextButton('overall_rating', rating);
  }
  function handleGenreButton(rating){
    setSelection(rating);
    handleNextButton('genre_rating', rating)
  }
  function handleMoodButton(rating){
    setSelection(rating);
    handleNextButton('mood_rating', rating)
  }
  function handleVocalButton(rating){
    setSelection(rating);
    handleNextButton('vocal_timbre_rating', rating)
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