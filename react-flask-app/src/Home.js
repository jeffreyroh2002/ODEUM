import React, { useState, useEffect } from 'react';
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

  const handleLogout = () => {
    // Perform logout logic, e.g., clear tokens, reset state, etc.
    setIsLoggedIn(false); // Update the logged-in state to false
  };

  

  return (
    <div>
      <Header isLoggedIn={isLoggedIn} onLogout={handleLogout} />
      <div className="home-container">
        <div className="main-content">
          <h2 className="sub-title">Unlock your True <br/> Musical Taste with <span className="gradient-text">AI</span></h2>
          <h2 className="sub-text">Take a free test and receive a detailed analysis on your one-of-a-kind musical personality</h2>
          <Link
            to={isLoggedIn ? "/beforeTest" : "/login"} // Conditional routing based on isLoggedIn
            className="cta-button"
          >
            Take Test
          </Link>
          {!isLoggedIn && (
            <Link to="/Signup" className="cta-button">
              Learn More
            </Link>
          )}
          <h2 className='sub-header'>Image for Reference</h2>
          <h2 className='sub-header'>text-text-text</h2>
          <h2 className='sub-header'>Our Technology</h2>
          <h2 className='sub-header'>text-text-text</h2>

        </div>
      </div>
    </div>
  );
}