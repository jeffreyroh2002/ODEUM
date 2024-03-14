import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import empty_blue_circle from "../images/empty-blue-circle.png";
import empty_red_circle from "../images/empty-red-circle.png";
import filled_blue_circle from "../images/filled-blue-circle.png";
import filled_red_circle from "../images/filled-red-circle.png";
import prev_button from "../images/prev_button.png"
import next_button from "../images/next_button.png"

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

  const handleSelection = (category, value) => {
    setSelections(prev => ({
      ...prev,
      [category]: prev[category] === value ? 0 : value, // Toggle selection
    }));
  };

  const getImageStyle = (option) => {
    const sizeMap = {
      "-3": { width: "50px", height: "50px" },
      "-2": { width: "40px", height: "40px" },
      "-1": { width: "30px", height: "30px" },
      "1": { width: "30px", height: "30px" },
      "2": { width: "40px", height: "40px" },
      "3": { width: "50px", height: "50px" },
    };
    return sizeMap[option.toString()] || { width: "30px", height: "30px" };
  };

  const getImage = (value, isSelected) => {
    if (value <= 0) {
      return isSelected ? filled_red_circle : empty_red_circle;
    } else {
      return isSelected ? filled_blue_circle : empty_blue_circle;
    }
  };

  const renderOptions = (category, options) => {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        {options.map(value => {
          const isSelected = selections[category] === value;
          return (
            <button
              key={value}
              onClick={() => handleSelection(category, value)}
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
              }}
            >
              <img src={getImage(value, isSelected)} alt={`Rating ${value}`}
                   style={getImageStyle(value)} />
            </button>
          );
        })}
      </div>
    );
  };

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
    if (currentQuestionIndex < 3) {
      onNextQuestion() // Go to next question
    } else {
      // All questions are answered, load new audio file or navigate to completion page
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


  return (
    <div>
      {/* Render questions based on currentQuestionIndex */}
      {currentQuestionIndex === 0 && (
        <div className="rating-group">
          <h4 className="rating--label">Rate the Song.</h4>
          {renderOptions('overallRating', [-3, -2, -1, 1, 2, 3])}
        </div>
      )}

      {currentQuestionIndex === 1 && (
        <div className="rating-group">
          <h4 className="rating--label">What do you think of the 'Genre' of this song?</h4>
          {renderOptions('genreRating', [-3, -2, -1, 1, 2, 3])}
        </div>
      )}

      {currentQuestionIndex === 2 && (
        <div className="rating-group">
          <h4 className="rating--label">What do you think of the 'Mood' of this song?</h4>
          {renderOptions('moodRating', [-3, -2, -1, 1, 2, 3])}
        </div>
      )}

      {currentQuestionIndex === 3 && (
        <div className="rating-group">
          <h4 className="rating--label">What do you think of the 'Vocals' of this song?</h4>
          {renderOptions('vocalRating', [-3, -2, -1, 1, 2, 3])}
        </div>
      )}

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