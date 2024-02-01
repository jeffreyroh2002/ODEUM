import React from "react";

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

  function handleChange(event) {a
    const { name, value, type, checked } = event.target;
    setFormData((prevFormData) => {
      return {
        ...prevFormData,
        [name]: type === "checkbox" ? checked : parseInt(value, 10),
      };
    });
  }

  return (
    <form>
      <label>Overall Rating:</label>
      <input
        type="radio"
        id="-3"
        name="overallRating"
        value="-3"
        checked={formData.overallRating === -3}
        onChange={handleChange}
      />
      <label htmlFor="-3">-3</label>

      <input
        type="radio"
        id="-2"
        name="overallRating"
        value="-2"
        checked={formData.overallRating === -2}
        onChange={handleChange}
      />
      <label htmlFor="-2">-2</label>

      <input
        type="radio"
        id="-1"
        name="overallRating"
        value="-1"
        checked={formData.overallRating === -1}
        onChange={handleChange}
      />
      <label htmlFor="-1">-1</label>

      <input
        type="radio"
        id="1"
        name="overallRating"
        value="1"
        checked={formData.overallRating === 1}
        onChange={handleChange}
      />
      <label htmlFor="1">1</label>

      <input
        type="radio"
        id="2"
        name="overallRating"
        value="2"
        checked={formData.overallRating === 2}
        onChange={handleChange}
      />
      <label htmlFor="2">2</label>

      <input
        type="radio"
        id="3"
        name="overallRating"
        value="3"
        checked={formData.overallRating === 3}
        onChange={handleChange}
      />
      <label htmlFor="3">3</label>
    </form>
  );
}
