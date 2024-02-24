import React, { useState, useEffect } from 'react';
import { withRouter } from 'react-router-dom';
import Header from "./components/Header"
import { Link } from 'react-router-dom';
import './Home.css';
import axios from 'axios';


export default function Home() {

  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Fetch isLoggedIn status from backend when component mounts
    axios.get('/isLoggedIn')
      .then(response => {
        setIsLoggedIn(response.data.isLoggedIn);
      })
      .catch(error => {
        console.error('Error fetching isLoggedIn status:', error);
      });
  }, []);

  return (
    <div>
      <Header />
      <div className="home-container">
        <div className="main-content">
          <h1 className="main-title">ODEUM</h1>
          <p className="sub-title">Unraveling the Personalized Tapestry of Musical Taste</p>
          <Link 
            to={isLoggedIn ? "/questionnaire" : "/login"} // Conditional routing based on isLoggedIn
            className="cta-button"
          >
            Take Free Music Personality Test
          </Link>
          {!isLoggedIn && (
            <Link to="/Signup" className="cta-button">
              Sign Up Now
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}