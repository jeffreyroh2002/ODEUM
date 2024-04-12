import React, { useState, useEffect } from 'react';
import Header from "./components/Header"
import { Link } from 'react-router-dom';
import './ArtistSelector.css';
import axios from 'axios';

function ArtistCard({ artist, onSelectArtist }) {
  return (
    <div className="artist-card" onClick={() => onSelectArtist(artist.id)}>
      <img src={artist.imageUrl} alt={artist.name} style={{ width: 100, height: 100 }} />
      <h3>{artist.name}</h3>
    </div>
  );
}

async function fetchArtists(token) {
  const response = await axios.get('https://api.spotify.com/v1/browse/new-releases', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.data.albums.items.map(album => ({
    id: album.artists[0].id,
    name: album.artists[0].name,
    imageUrl: album.images[0].url
  }));
}

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
    if (token) {
      fetchArtists(token).then(setArtists);
    }
  }, [token]);

  const handleSelectArtist = artistId => {
    fetchRelatedArtists(artistId, token).then(setArtists);
  };

  return (
    <div>
      <Header />
      {artists.map(artist => (
        <ArtistCard key={artist.id} artist={artist} onSelectArtist={handleSelectArtist} />
      ))}
    </div>
  );
}

export default ArtistSelector;