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

  

  return (
    <div>
      <Header />
      <div className="home-container">
        <div className="main-content">
          <h2 className="sub-title">Unlock your True Musical Taste<br/>with <span className="gradient-text">AI</span></h2>
          <h3 className="sub-text">Take a free test and receive a detailed analysis <br /> on your one-of-a-kind musical personality</h3>
          <Link
            to={isLoggedIn ? "/beforeTest" : "/login"} // Conditional routing based on isLoggedIn
            className="cta-button"
          >
            Take Free Test
          </Link>
          {!isLoggedIn && (
            <Link to="/Signup" className="cta-button">
              Sign Up Now
            </Link>
          )}
          <h2 className='sub-header'>Our Technology</h2>
        </div>
      </div>
    </div>
  );
}