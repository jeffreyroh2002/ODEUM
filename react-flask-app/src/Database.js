import React, { useState, useEffect } from 'react';

function Database() {
  const BASE_URL = process.env.REACT_APP_API_BASE_URL;
  const [audioFiles, setAudioFiles] = useState([]);

  useEffect(() => {
    fetch(`${BASE_URL}/print_db`)
      .then(res => res.json())
      .then(data => {
        setAudioFiles(data); // Assuming the response contains an array of audio files
      })
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="App">
      <h1>Audio Files:</h1>
      <ul>
        {audioFiles.map((audioFile, index) => (
          <li key={index}>
            <p>Audio Name: {audioFile.audio_name}</p>
            <p>File Path: {audioFile.file_path}</p>
            <p>Genre: {audioFile.genre}</p>
            <p>Mood: {audioFile.mood}</p>
            <p>Vocal: {audioFile.vocal}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Database;
