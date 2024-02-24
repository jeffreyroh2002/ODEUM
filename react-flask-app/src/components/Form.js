import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import empty_blue_circle from "../images/empty-blue-circle.png";
import empty_red_circle from "../images/empty-red-circle.png";
import filled_blue_circle from "../images/filled-blue-circle.png";
import filled_red_circle from "../images/filled-red-circle.png";
import prev_button from "../images/prev_button.png"
import next_button from "../images/next_button.png"

export default function Form({ audioFileId, testType, onNextAudioFile }) {
  const navigate = useNavigate();
  const [selections, setSelections] = useState({
    overallRating: null,
    genreRating: 0,
    moodRating: 0,
    vocalRating: 0,
  });

  const [csrfToken, setCsrfToken] = useState('');

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

  function handlePrevButton(){
    //reset page to prev question
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
        test_id: testType,
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
        if (nextAudioFileId) {
            onNextAudioFile(nextAudioFileId); // Call the callback function with the next audio file id
        } else {
            navigate('/TestCompleted');
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
        {renderOptions('overallRating', [-3, -2, -1, 1, 2, 3])}
      </div>

      <div className="line-with-text">
            <hr />
            <div className="text">Optional Questions</div>
        </div>
        <p className="gray">**Leave field(s) as empty if unsure**</p>
      
      <div className="rating-group">
        <h4 className="rating--label">What do you think of the 'Genre' of this song?</h4>
        {renderOptions('genreRating', [-3, -2, -1, 1, 2, 3])}
      </div>
      <div className="rating-group">
        <h4 className="rating--label">What do you think of the 'Mood' of this song?</h4>
        {renderOptions('moodRating', [-3, -2, -1, 1, 2, 3])}
      </div>
      <div className="rating-group">
        <h4 className="rating--label">What do you think of the 'Vocals' of this song?</h4>
        {renderOptions('vocalRating', [-3, -2, -1, 1, 2, 3])}
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
