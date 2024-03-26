import React, { useState, useEffect } from 'react';
import './Form.css';
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

export default function Form({ testId, questionIndex, onPrevButton, onNextButton, audiosNum, questionsNum, onQuit, onTestSubmit}) {
  const [csrfToken, setCsrfToken] = useState('');
  const MySwal = withReactContent(Swal)

  const selection_types = ['vocal_timbre_rating', 'overall_rating', 'genre_rating', 'mood_rating']
  const selection_type = selection_types[questionIndex % questionsNum]

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
    console.log(questionIndex)

    if (questionIndex % questionsNum === 1 && type_rating === undefined) {
      MySwal.fire({
        icon: "error",
        title: "This question is required!",
      });
    }
    
    else {
      if (type_rating === undefined) type_rating = 0
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
      onNextButton();
    }
  }

  return (
    <div>
      <div className="rating--container">
        {/* Render questions based on currentQOKuestionIndex */}
        {questionIndex % questionsNum === 1 && (
          <div className="rating-group">
            <h4 className="rating--label">Rate the Song.</h4>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 3)}>could listen to it all day &#128293;</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 2)}>pretty decent</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 1)}>could get used to it</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, -1)}>would not play it myself</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, -2)}>eh...</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, -3)}>hate it with a passion &#128556;</button>
          </div>
        )}

        {questionIndex % questionsNum === 2 && (
          <div className="rating-group">
            <h4 className="rating--label">How is the Genre?</h4>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 3)}>Fire</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 2)}>Decent</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 1)}>Not bad</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, -1)}>Would not play it myself</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, -2)}>eh...</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, -3)}>Hate it</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 0)}>Not sure &#x1f937;</button>
          </div>
        )}

        {questionIndex % questionsNum === 3 && (
          <div className="rating-group">
            <h4 className="rating--label">Describe the vibe or feeling of this song.</h4>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 3)}>Fire</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 2)}>Decent</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 1)}>Not bad</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, -1)}>Would not play it myself</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, -2)}>eh...</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, -3)}>Hate it </button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 0)}>Not sure &#x1f937;</button>
          </div>
        )}

        {questionIndex % questionsNum === 0 && (
          <div className="rating-group">
            <h4 className="rating--label">Thoughts on the vocals?</h4>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 3)}>Fire</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 2)}>Decent</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 1)}>Not bad</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, -1)}>Would not play it myself</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, -2)}>eh...</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, -3)}>Hate it</button>
            <button className="rating--button" onClick={() => handleSelection(selection_type, 0)}>Not sure &#x1f937;</button>
          </div>
        )}
      </div>
      
      {questionIndex === 1 ? 
        <button className="quit--button" onClick={onQuit}>Quit Test</button> :
        <button className="prev--button" onClick={onPrevButton}>Previous Button</button>}

      {questionIndex ===  audiosNum * questionsNum ?  
        <button className="submit--button" onClick={() => handleSelection(selection_type, undefined)}>Submit Test</button> :
        <button className="next--button" onClick={() => handleSelection(selection_type, undefined)}>Next Button</button>}

    </div>
  );
}