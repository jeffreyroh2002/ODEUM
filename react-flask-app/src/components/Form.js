import React from "react";
import empty_blue_circle from "../images/empty-blue-circle.png";
import empty_red_circle from "../images/empty-red-circle.png";
import filled_blue_circle from "../images/filled-blue-circle.png";
import filled_red_circle from "../images/filled-red-circle.png";

export default function Form() {
  const [formData, setFormData] = React.useState({
    overallRating: 0,
    genreRating: 0,
    moodRating: 0,
    vocalRating: 0,
    noGenre: false,
    noMood: false,
    noVocal: false,
  });

  function handleChange(event) {
    const { name, value, type, checked } = event.target;
    setFormData((prevFormData) => {
      return {
        ...prevFormData,
        [name]: type === "checkbox" ? checked : parseInt(value, 10),
      };
    });
  }

  const getImageStyle = (option) => {
    let style = {};

    // Adjust image size based on option
    if (option === -3) {
      style.width = "50px"; 
      style.height = "50px"; 
    } else if (option === -2) {
      style.width = "40px"; 
      style.height = "40px"; 
    } else if (option === -1) {
        style.width = "30px"; 
        style.height = "30px";
    } else if (option === 1) {
        style.width = "30px"; 
        style.height = "30px";
    } else if (option === 2) {
        style.width = "40px"; 
        style.height = "40px"; 
    } else if (option === 3){
        style.width = "50px";
        style.height = "50px";
    }

    return style;
  };

  const renderCustomRadioButtons = (name, options) => {
    return options.map((option) => (
      <div key={option} className="custom-radio">
        <input
          type="radio"
          id={`${name}-${option}`}
          name={name}
          value={option}
          checked={formData[name] === option}
          onChange={handleChange}
        />
        <label htmlFor={`${name}-${option}`} className="custom-radio-label">
          {formData[name] === option ? (
            <img
              src={
                option <= 0
                  ? filled_red_circle // Use imported variable directly
                  : filled_blue_circle // Use imported variable directly
              }
              alt={`Rating ${option}`}
              style={getImageStyle(option)} // Apply inline styles
            />
          ) : (
            <img
              src={
                option <= 0
                  ? empty_red_circle // Use imported variable directly
                  : empty_blue_circle // Use imported variable directly
              }
              alt={`Rating ${option}`}
              style={getImageStyle(option)} // Apply inline styles
            />
          )}
        </label>
      </div>
    ));
  };

  return (
    <form>
        <div className="rating-group">
            <label className="rating--label">Rate the Song.</label>
            <div className="radio-buttons">
                {renderCustomRadioButtons("overallRating", [-3, -2, -1, 1, 2, 3])}
            </div>
        </div>

        <div class="line-with-text">
            <hr />
            <div class="text">Optional Questions</div>
        </div>

        <div className="rating-group">
            <label>What do you think of the 'Genre' of this song?</label>
            <div className="radio-buttons">
                {renderCustomRadioButtons("genreRating", [-3, -2, -1, 1, 2, 3])}
            </div>
        </div>

        <div className="rating-group">
            <label>What do you think of the 'Mood' of this song?</label>
            <div className="radio-buttons">
                {renderCustomRadioButtons("moodRating", [-3, -2, -1, 1, 2, 3])}
            </div>
        </div>

        <div className="rating-group">
            <label>What do you think of the 'Vocals' of this song?</label>
            <div className="radio-buttons">
                {renderCustomRadioButtons("vocalRating", [-3, -2, -1, 1, 2, 3])}
            </div>
        </div>
        
    </form>
  );
}