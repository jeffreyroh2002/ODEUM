import React, { useState, useEffect } from 'react';
import Header from "./components/Header"
import { Link } from 'react-router-dom';
import './ArtistSelector.css';
import axios from 'axios';


async function fetchRelatedArtists(artistId, token) {
  const response = await axios.get(`https://api.spotify.com/v1/artists/${artistId}/related-artists`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.data.artists.map(artist => ({
    id: artist.id,
    name: artist.name,
    imageUrl: artist.images[0].url
  }));
}

function ArtistSelector() {
  const [artists, setArtists] = useState([]);
  const [token, setToken] = useState('');

  useEffect(() => {
    // Fetch token from Flask backend
    axios.get('/get-token')  // Adjust the URL to where your Flask app is hosted
      .then(response => {
        setToken(response.data.access_token);
      })
      .catch(error => console.error('Error fetching token:', error));
  }, []);

  useEffect(() => {
    axios.get('/fetch-popular-artists')
      .then(response => {
        setArtists(response.data);
      })
      .catch(error => console.error('Error fetching artists:', error));
  }, []);

  const handleSelectArtist = artistId => {
    fetchRelatedArtists(artistId, token).then(setArtists);
  };

  return (
    <div>
      <Header />
      <div className="artist-container">
        {artists.map(artist => (
          <div className="artist-card" key={artist.id} onClick={() => handleSelectArtist(artist.id)} >
            <img src={artist.imageUrl} alt={artist.name} />
            <h3>{artist.name}</h3>
            <p>Popularity: {artist.popularity}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ArtistSelector;