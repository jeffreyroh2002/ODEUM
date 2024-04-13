import React, { useState, useEffect } from 'react';
import Header from "./components/Header"
import { Link } from 'react-router-dom';
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
  const [artists, setArtists] = useState([]);
  const [token, setToken] = useState('');
  const [selectedArtistIds, setSelectedArtistIds] = useState(new Set());

  useEffect(() => {
      axios.get('/get-token')  // Adjust the URL to where your Flask app is hosted
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
    // Toggle selection state
    setSelectedArtistIds(prevIds => {
        const newIds = new Set(prevIds); // Create a new Set based on the previous Set
        if (newIds.has(artistId)) {
            newIds.delete(artistId); // If the artist is already selected, deselect it
        } else {
            newIds.add(artistId); // Otherwise, add the artist to the selected Set
        }
        return newIds;
    });

    // Fetch and insert related artists
    fetchRelatedArtists(artistId, token).then(relatedArtists => {
        setArtists(prevArtists => {
            const existingIds = new Set(prevArtists.map(artist => artist.id)); // Create a set of existing artist IDs
            const index = prevArtists.findIndex(artist => artist.id === artistId);
            if (index === -1) return prevArtists; // If the artist isn't found, return the list unchanged

            // Filter out any related artists that are already in the list to avoid duplicates
            const newRelatedArtists = relatedArtists.filter(artist => !existingIds.has(artist.id));

            // Insert the new related artists next to the selected artist
            return [
                ...prevArtists.slice(0, index + 1),
                ...newRelatedArtists,
                ...prevArtists.slice(index + 1)
            ];
        });
    }).catch(error => {
        console.error('Error fetching related artists:', error);
    });
  };


  return (
    <div>
        <Header />
        <div className="artist-container">
            {artists.map(artist => (
                <div
                    className={`artist-card ${selectedArtistIds.has(artist.id) ? 'selected' : ''}`}
                    key={artist.id}
                    onClick={() => handleSelectArtist(artist.id)}
                >
                    <img src={artist.imageUrl} alt={artist.name} />
                    <h3>{artist.name}</h3>
                </div>
            ))}
        </div>
    </div>
  );
}

export default ArtistSelector;