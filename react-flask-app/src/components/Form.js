import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Form.css';

export default function Form({ audioFileId, testId, currentQuestionIndex, onAudioFile, setQuestion, onPrevQuestion, onNextQuestion }) {
  const navigate = useNavigate();
  const [selections, setSelections] = useState({
    overallRating: null,
    genreRating: 0,
    moodRating: 0,
    vocalRating: 0,
  });

  const [csrfToken, setCsrfToken] = useState('');


  useEffect(() => {
    console.log('Audio file id in Form:', audioFileId);
  }, [audioFileId]);

  useEffect(() => {
    console.log('testId in Form:', testId);
  }, [testId]);

  useEffect(() => {
    console.log('selections', selections);
  }, [selections]);


  // Fetch CSRF token on component mount if your Flask app has CSRF protection enabled
  useEffect(() => {
    fetch('/csrf-token').then(response => {
      return response.json();
    }).then(data => {
      setCsrfToken(data.csrf_token);
    });
  }, []);

  function handlePrevButton() {
    if (currentQuestionIndex > 0) {
      // If currentQuestionIndex is greater than 0, go to the previous question
      onPrevQuestion();
    } else {
      // If currentQuestionIndex is 0, fetch the previous audio file
      const prevForm = '/get_prev_questions';
      fetch(prevForm, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
          audio_id: audioFileId, 
          test_id: testId,
        }),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data.status === 'send_to_before_test') {
          // If the server response indicates to navigate to the BeforeTest page, do so
          navigate('/BeforeTest');
        } 
        else {
          const prevAudioFileId = data.prev_audio_file_id; // Extract next audio file id from server response
          console.log("prev audio file id: ", prevAudioFileId)
          if (prevAudioFileId) {
            // Load new audio file
            onAudioFile(prevAudioFileId);
            // Reset selections
            setSelections({
              overallRating: null,
              genreRating: 0,
              moodRating: 0,
              vocalRating: 0,
          });

          setQuestion(3);
          }
        }
      })
      .catch(error => {
        console.error('Error getting previous questions:', error);
        alert('There was an error getting previous questions. Please try again.');
      });
    }
  }
  
  

  // submitting to the Flask backend
  function handleNextButton() {
    if (currentQuestionIndex < 4) {
      onNextQuestion() // Go to next question
    } else {
      // All questions are answered, load new audio file or navigate to completion page
      const submitUrl = '/submit_answer';
      console.log("VOCAL_TIMBRE_RATING:", selections.vocalRating)
      fetch(submitUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken, // Assuming CSRF protection is enabled
        },
        body: JSON.stringify({
          overall_rating: selections.overallRating,
          genre_rating: selections.genreRating,
          mood_rating: selections.moodRating,
          vocal_timbre_rating: selections.vocalRating,
          audio_id: audioFileId, 
          test_id: testId,
        }),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        const nextAudioFileId = data.next_audio_file_id; // Extract next audio file id from server response
        const nextTestId = data.test_id;
  
        if (nextAudioFileId) {
          // Load new audio file
          onAudioFile(nextAudioFileId);
          // Reset selections
          setSelections({
            overallRating: null,
            genreRating: 0,
            moodRating: 0,
            vocalRating: 0,
          });
          // Reset question index to 0
          setQuestion(0);
        } else {
          // Navigate to test completion page
          navigate(`/TestCompleted?testId=${nextTestId}`, { replace: true });
        }
      })
      .catch(error => {
        console.error('Error submitting answers:', error);
        alert('There was an error submitting your answers. Please try again.');
      });
    }
  }

  function handleOverallButton(rating){
    setSelections({
      ...selections,
      overallRating: rating
    });
    handleNextButton()
  }

  function handleGenreButton(rating){
    setSelections({
      ...selections,
      genreRating: rating
    });
    handleNextButton()
  }
  function handleMoodButton(rating){
    setSelections({
      ...selections,
      moodRating: rating
    });
    handleNextButton()
  }
  function handleVocalButton(rating){
    setSelections({
      ...selections,
      vocalRating: rating
    });
    handleNextButton()
  }

  return (
    <div>
      <div className="rating--container">
        {/* Render questions based on currentQuestionIndex */}
        {currentQuestionIndex === 0 && (
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

        {currentQuestionIndex === 1 && (
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

        {currentQuestionIndex === 2 && (
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

        {currentQuestionIndex === 3 && (
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