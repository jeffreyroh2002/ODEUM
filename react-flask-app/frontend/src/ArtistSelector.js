import React, { useState, useEffect } from 'react';
import Header from "./components/Header"
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import './ArtistSelector.css';
import axios from 'axios';


async function fetchArtists(token) {
  const genres = ['pop', 'rock', 'hip-hop', 'jazz', 'electronic', 'rnb', 'indie']; // Example genres
  const markets = ['US', 'KR']; // United States and South Korea
  let artists = [];
  let artistIds = new Set(); // To avoid duplicating artists

  for (const market of markets) {
      for (const genre of genres) {
          const response = await axios.get('https://api.spotify.com/v1/search', {
              headers: { 'Authorization': `Bearer ${token}` },
              params: {
                  q: `genre:"${genre}"`,
                  type: 'artist',
                  market: market,
                  limit: 3  // Limit the number of artists fetched per genre to balance the total number
              }
          });
          const fetchedArtists = response.data.artists.items;
          fetchedArtists.forEach(artist => {
              if (!artistIds.has(artist.id)) { // Check if artist is already added
                  artists.push({
                      id: artist.id,
                      name: artist.name,
                      imageUrl: artist.images[0] ? artist.images[0].url : undefined,
                      popularity: artist.popularity || 'N/A'
                  });
                  artistIds.add(artist.id);
              }
          });
      }
  }

  return artists; // Return a flat list of unique artists
}

async function fetchRelatedArtists(artistId, token) {
  const response = await axios.get(`https://api.spotify.com/v1/artists/${artistId}/related-artists`, {
      headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.data.artists.slice(0, 5).map(artist => ({
      id: artist.id,
      name: artist.name,
      imageUrl: artist.images[0] ? artist.images[0].url : undefined
  }));
}

function ArtistSelector() {
  const BASE_URL = process.env.REACT_APP_API_BASE_URL;

  const navigate = useNavigate();
  const [artists, setArtists] = useState([]);
  const [token, setToken] = useState('');
  const [selectedArtistIds, setSelectedArtistIds] = useState([]);
  const [csrfToken, setCsrfToken] = useState('');

  useEffect(() => {
    axios.get(`${BASE_URL}/csrf-token`).then(response => {
      setCsrfToken(response.data.csrf_token);
    });
  }, []);

  useEffect(() => {
      axios.get(`${BASE_URL}/get-token`)  // Adjust the URL to where your Flask app is hosted
          .then(response => {
              setToken(response.data.access_token);
          })
          .catch(error => console.error('Error fetching token:', error));
  }, []);

  useEffect(() => {
      if (token) {
          fetchArtists(token).then(artists => setArtists(artists))
              .catch(error => console.error('Error fetching artists:', error));
      }
  }, [token]);

  const handleSelectArtist = artistId => {
    setSelectedArtistIds(prevIds => {
      const index = prevIds.indexOf(artistId);
      if (index > -1) {
        return prevIds.filter(id => id !== artistId);
      } else {
        fetchRelatedArtists(artistId, token).then(relatedArtists => {
          const newArtists = artists.slice(); // Make a shallow copy of the array
          const insertAt = newArtists.findIndex(artist => artist.id === artistId) + 1;
          relatedArtists.forEach(relatedArtist => {
            if (!newArtists.find(a => a.id === relatedArtist.id)) {
              newArtists.splice(insertAt, 0, relatedArtist); // Insert related artists right after the selected one
            }
          });
          setArtists(newArtists);
        }).catch(error => console.error('Error fetching related artists:', error));
        return [...prevIds, artistId];
      }
    });
  };

  const handleSubmit = () => {
    axios.post(`${BASE_URL}/submit_artists`, { selectedArtistIds },
        {headers: {
            'X-CSRF-Token': csrfToken
          }
        }).then(response => {
            console.log('Answers selected successfully:', response.data);
      }).catch(error => console.error('Error submitting artists:', error));
    navigate(`/BeforeTest`)
  };

  return (
    <div>
        <Header />
        <div className="artist-container">
            {artists.map(artist => (
                <div
                className={`artist-card ${selectedArtistIds.includes(artist.id) ? 'selected' : ''}`}
                    key={artist.id}
                    onClick={() => handleSelectArtist(artist.id)}
                >
                    <img src={artist.imageUrl} alt={artist.name} />
                    <h3>{artist.name}</h3>
                </div>
            ))}
        </div>
        <button className="submit--button" onClick={handleSubmit}>
            Finish Selection
      </button>
    </div>
  );
}

export default ArtistSelector;