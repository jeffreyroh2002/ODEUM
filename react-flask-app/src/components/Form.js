import React, { useState, useEffect } from 'react';
import './Form.css';
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import axios from 'axios'

export default function Form({ testId, questionIndex, onPrevButton, onNextButton, audiosNum, questionsNum, onQuit, onTestSubmit}) {
  const [csrfToken, setCsrfToken] = useState('');
  const MySwal = withReactContent(Swal)
  const [savedRating, setSavedRating] = useState();
  const selectionTypes = ['vocal_timbre_rating', 'overall_rating', 'genre_rating', 'mood_rating']
  const [selectionType, setSelectionType] = useState(selectionTypes[questionIndex % questionsNum])
  const buttons = document.querySelectorAll('.rating--button')
  // Fetch CSRF token on component mount if your Flask app has CSRF protection enabled
  useEffect(() => {
    fetch('/csrf-token').then(response => {
      return response.json();
    }).then(data => {
      setCsrfToken(data.csrf_token);
    });
  }, []);

  useEffect(() => {
    axios.get(`/get_useranswer?question_index=${questionIndex}&test_id=${testId}`)
         .then(response => {
            console.log("response rating: ",response.data.rating);
            setSavedRating(parseInt(response.data.rating));
         })
         .catch(error => {console.log("error in fetching useranswer data: ", error)});
    setSelectionType(selectionTypes[questionIndex % questionsNum]);
  }, [questionIndex])

  useEffect(() => {
    buttons.forEach(button => { button.classList.remove('yellow-background'); });
    switch(savedRating) {
      case 3:
          document.getElementById(`button1`).classList.add('yellow-background');
          break;
      case 2:
          document.getElementById(`button2`).classList.add('yellow-background');
          break;
      case 1:
          document.getElementById(`button3`).classList.add('yellow-background');
          break;
      case -1:
          document.getElementById(`button4`).classList.add('yellow-background');
          break;
      case -2:
          document.getElementById(`button5`).classList.add('yellow-background');
          break;
      case -3:
          document.getElementById(`button6`).classList.add('yellow-background');
          break;
      case 0:
          console.log("no selection => default 0");
          break;
      default:
          console.log("No valid selection");
    }
  }, [savedRating])

  function handleSelection(rating) { setSavedRating(rating); }
  // submitting to the Flask backend

  function handleSelectionSubmit() {
    if (questionIndex % questionsNum === 1 && !savedRating) {
      MySwal.fire({
        icon: "error",
        title: "This question is required!",
      });
    }
    
    else {
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
          type: selectionType,
          rating: (savedRating ? savedRating : 0)
        })
      })
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
            <button id="button1" className="rating--button" onClick={() => handleSelection(3)}>could listen to it all day &#128293;</button>
            <button id="button2" className="rating--button" onClick={() => handleSelection(2)}>pretty decent</button>
            <button id="button3" className="rating--button" onClick={() => handleSelection(1)}>could get used to it</button>
            <button id="button4" className="rating--button" onClick={() => handleSelection(-1)}>would not play it myself</button>
            <button id="button5" className="rating--button" onClick={() => handleSelection(-2)}>eh...</button>
            <button id="button6" className="rating--button" onClick={() => handleSelection(-3)}>hate it with a passion &#128556;</button>
          </div>
        )}

        {questionIndex % questionsNum === 2 && (
          <div className="rating-group">
            <h4 className="rating--label">How is the Genre?</h4>
            <button id="button1" className="rating--button" onClick={() => handleSelection(3)}>Fire</button>
            <button id="button2" className="rating--button" onClick={() => handleSelection(2)}>Decent</button>
            <button id="button3" className="rating--button" onClick={() => handleSelection(1)}>Not bad</button>
            <button id="button4" className="rating--button" onClick={() => handleSelection(-1)}>Would not play it myself</button>
            <button id="button5" className="rating--button" onClick={() => handleSelection(-2)}>eh...</button>
            <button id="button6" className="rating--button" onClick={() => handleSelection(-3)}>Hate it</button>
          </div>
        )}

        {questionIndex % questionsNum === 3 && (
          <div className="rating-group">
            <h4 className="rating--label">Describe the vibe or feeling of this song.</h4>
            <button id="button1" className="rating--button" onClick={() => handleSelection(3)}>Fire</button>
            <button id="button2" className="rating--button" onClick={() => handleSelection(2)}>Decent</button>
            <button id="button3" className="rating--button" onClick={() => handleSelection(1)}>Not bad</button>
            <button id="button4" className="rating--button" onClick={() => handleSelection(-1)}>Would not play it myself</button>
            <button id="button5" className="rating--button" onClick={() => handleSelection(-2)}>eh...</button>
            <button id="button6" className="rating--button" onClick={() => handleSelection(-3)}>Hate it </button>
          </div>
        )}

        {questionIndex % questionsNum === 0 && (
          <div className="rating-group">
            <h4 className="rating--label">Thoughts on the vocals?</h4>
            <button id="button1" className="rating--button" onClick={() => handleSelection(3)}>Fire</button>
            <button id="button2" className="rating--button" onClick={() => handleSelection(2)}>Decent</button>
            <button id="button3" className="rating--button" onClick={() => handleSelection(1)}>Not bad</button>
            <button id="button4" className="rating--button" onClick={() => handleSelection(-1)}>Would not play it myself</button>
            <button id="button5" className="rating--button" onClick={() => handleSelection(-2)}>eh...</button>
            <button id="button6" className="rating--button" onClick={() => handleSelection(-3)}>Hate it</button>
          </div>
        )}
      </div>
      
      {questionIndex === 1 ? 
        <button className="quit--button" onClick={onQuit}>Quit Test</button> :
        <button className="prev--button" onClick={onPrevButton}>Previous Button</button>}

      {questionIndex ===  audiosNum * questionsNum ?  
        <button className="submit--button" onClick={() => handleSelectionSubmit()}>Submit Test</button> :
        <button className="next--button" onClick={() => handleSelectionSubmit()}>Next Button</button>}

    </div>
  );
}