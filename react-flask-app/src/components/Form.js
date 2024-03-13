import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import empty_blue_circle from "../images/empty-blue-circle.png";
import empty_red_circle from "../images/empty-red-circle.png";
import filled_blue_circle from "../images/filled-blue-circle.png";
import filled_red_circle from "../images/filled-red-circle.png";
import prev_button from "../images/prev_button.png"
import next_button from "../images/next_button.png"

export default function Form({ audioFileId, testId, onAudioFile }) {
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

  function handleSurveyButton(){
    // handle function here
  }

  function handlePrevButton(){
    const prevForm = '/get_prev_questions';
    fetch(prevForm, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken, // Assuming CSRF protection is enabled
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
      console.log(data); // Add this line to check the structure of the response data
      
      if (data.status === 'in_progress') {
        const { overall_rating, genre_rating, mood_rating, vocal_timbre_rating } = data;
        setSelections({
          overallRating: overall_rating,
          genreRating: genre_rating,
          moodRating: mood_rating,
          vocalRating: vocal_timbre_rating,
        });
        onAudioFile(data.prev_audio_file_id);

      } else if (data.status === 'send_to_before_test') {
          navigate('/BeforeTest');
      } else {
          throw new Error('Unexpected server response');
      }
    })
    .catch(error => {
      console.error('Error submitting answers:', error);
      alert('There was an error submitting your answers. Please try again.');
    });
  }

  // submitting to the Flask backend
  function handleNextButton() {
    const submitUrl = '/submit_answer';

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
        console.log(data); // Add this line to check the structure of the response data
        const nextAudioFileId = data.next_audio_file_id; // Extract next audio file id from server response
        const testId = data.test_id;
        if (nextAudioFileId) {
          const { overall_rating, genre_rating, mood_rating, vocal_timbre_rating } = data;
          setSelections({
            overallRating: overall_rating,
            genreRating: genre_rating,
            moodRating: mood_rating,
            vocalRating: vocal_timbre_rating,
          });
          onAudioFile(nextAudioFileId); 
        } else {
          navigate(`/TestCompleted?testId=${testId}`, { replace: true });
        }
    })
    .catch(error => {
      console.error('Error submitting answers:', error);
      alert('There was an error submitting your answers. Please try again.');
    });

  }


  return (
    <div>
      <div className="rating-group">
        <h4 className="rating--label">Rate the Song.</h4>
        <div className="button--container">
            <button onClick={handleSurveyButton}>Q1</button>
            <button onClick={handleSurveyButton}>Q2</button>
            <button onClick={handleSurveyButton}>Q3</button>
            <button onClick={handleSurveyButton}>Q4</button>
            <button onClick={handleSurveyButton}>Q5</button>
            <button onClick={handleSurveyButton}>Q6</button>
        </div>
      </div>

      <div className="button--container">
        <button className="prev--button" onClick={handlePrevButton}>
          <img src={prev_button} alt="Previous Button" />
        </button>

        <button className="next--button" onClick={handleNextButton}>
          <img src={next_button} alt="Next Button" />
        </button>
      </div>

    </div>
  );
}