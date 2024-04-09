import React, { useState, useEffect } from 'react';
import './Form.css';
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import axios from 'axios'

export default function Form({testId, questionIndex, audioId, onPrevQuestion, onNextQuestion, numQ, onQuit, questionType}) {
  const [csrfToken, setCsrfToken] = useState('');
  const MySwal = withReactContent(Swal);
  const ratingsButtons = {'3' : 'button1', '2' : 'button2', '1': 'button3', '-1' : 'button4', '-2' : 'button5', '-3' : 'button6'};
  const selectedClass = 'yellow-background';
  const [savedRating, setSavedRating] = useState();

  useEffect(() => {
    fetch('/csrf-token').then(response => {
      return response.json();
    }).then(data => {
      setCsrfToken(data.csrf_token);
    });
    console.log("please: ", audioId, questionType, testId)
    axios.get(`/get_useranswer?audio_id=${audioId}&question_type=${questionType}&test_id=${testId}`)
    .then(response => {
       const rating = response.data.rating;
       let button;
       if (rating) {
         button = document.getElementById(ratingsButtons[rating.toString()]);
         setSavedRating(rating);
       }
       else setSavedRating(0);
       if (button) button.classList.add(selectedClass); 
     })
    .catch(error => {console.log("error in fetching useranswer data: ", error)});
  }, []);


  function onSelectionClick(rating) {
    const button = document.getElementById(ratingsButtons[rating.toString()]);
    if (button.classList.contains(selectedClass)) {
      button.classList.remove(selectedClass);
      setSavedRating(0);
    }
    else {
      button.classList.add(selectedClass);
      setSavedRating(rating);
      submitAnswer(questionIndex, rating);
    };
  };

  function submitAnswer(questionIndex, rating) {
    if (questionType === 'overall_rating' && !rating) {
      MySwal.fire({
        icon: "error",
        title: "This question is required!",
      });
    }
    else {
      fetch('/submit_answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
          test_id: testId,
          question_index: questionIndex,
          type: questionType,
          audio_id: audioId,
          rating: rating
        })
      });
      onNextQuestion();
    };
  };



  return (
    <div>
      <div className="rating--container">
        {/* Render questions based on currentQOKuestionIndex */}
        {questionType === 'overall_rating' && (
          <div className="rating-group">
            <h4 className="rating--label">Rate the Song.</h4>
            <button id="button1" className="rating--button" onClick={() => {onSelectionClick(3); }}>could listen to it all day &#128293;</button>
            <button id="button2" className="rating--button" onClick={() => {onSelectionClick(2); }}>pretty decent</button>
            <button id="button3" className="rating--button" onClick={() => {onSelectionClick(1); }}>could get used to it</button>
            <button id="button4" className="rating--button" onClick={() => {onSelectionClick(-1); }}>would not play it myself</button>
            <button id="button5" className="rating--button" onClick={() => {onSelectionClick(-2); }}>eh...</button>
            <button id="button6" className="rating--button" onClick={() => {onSelectionClick(-3); }}>hate it with a passion &#128556;</button>
          </div>
        )}

        {questionType === 'genre_rating' && (
          <div className="rating-group">
            <h4 className="rating--label">How is the Genre?</h4>
            <button id="button1" className="rating--button" onClick={() => {onSelectionClick(3); }}>Fire</button>
            <button id="button2" className="rating--button" onClick={() => {onSelectionClick(2); }}>Decent</button>
            <button id="button3" className="rating--button" onClick={() => {onSelectionClick(1); }}>Not bad</button>
            <button id="button4" className="rating--button" onClick={() => {onSelectionClick(-1); }}>Would not play it myself</button>
            <button id="button5" className="rating--button" onClick={() => {onSelectionClick(-2); }}>eh...</button>
            <button id="button6" className="rating--button" onClick={() => {onSelectionClick(-3); }}>Hate it</button>
          </div>
        )}
  
        {questionType === 'mood_rating' && (
          <div className="rating-group">
            <h4 className="rating--label">Describe the vibe or feeling of this song.</h4>
            <button id="button1" className="rating--button" onClick={() => {onSelectionClick(3); }}>Fire</button>
            <button id="button2" className="rating--button" onClick={() => {onSelectionClick(2); }}>Decent</button>
            <button id="button3" className="rating--button" onClick={() => {onSelectionClick(1); }}>Not bad</button>
            <button id="button4" className="rating--button" onClick={() => {onSelectionClick(-1); }}>Would not play it myself</button>
            <button id="button5" className="rating--button" onClick={() => {onSelectionClick(-2); }}>eh...</button>
            <button id="button6" className="rating--button" onClick={() => {onSelectionClick(-3); }}>Hate it </button>
          </div>
        )}

        {questionType === 'vocal_timbre_rating' && (
          <div className="rating-group">
            <h4 className="rating--label">Thoughts on the vocals?</h4>
            <button id="button1" className="rating--button" onClick={() => {onSelectionClick(3); }}>Fire</button>
            <button id="button2" className="rating--button" onClick={() => {onSelectionClick(2); }}>Decent</button>
            <button id="button3" className="rating--button" onClick={() => {onSelectionClick(1); }}>Not bad</button>
            <button id="button4" className="rating--button" onClick={() => {onSelectionClick(-1); }}>Would not play it myself</button>
            <button id="button5" className="rating--button" onClick={() => {onSelectionClick(-2); }}>eh...</button>
            <button id="button6" className="rating--button" onClick={() => {onSelectionClick(-3); }}>Hate it</button>
          </div>
        )}
      </div>
      
      {questionIndex === 1 ? 
        <button className="quit--button" onClick={onQuit}>Quit Test</button> :
        <button className="prev--button" onClick={onPrevQuestion}>Previous Button</button>}

      {questionIndex ===  numQ ?  
        <button className="submit--button" onClick={() => {submitAnswer(questionIndex, savedRating); } }>Submit Test</button> :
        <button className="next--button" onClick={() => {submitAnswer(questionIndex, savedRating); } }>Next Button</button>}
    </div>
  );
}