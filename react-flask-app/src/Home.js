import React from 'react';
import Header from "./components/Header"
import { Link } from 'react-router-dom';
import './Home.css';
import Typist from 'react-typist';

export default function Home() {

  /* For Typing Animation on main-content
  const [isTypingComplete, setIsTypingComplete] = React.useState(false);

  const handleTypingComplete = () => {
    setIsTypingComplete(true);
  };

  */

  return (
    <div>
      <Header />
      <div className="home-container">
        <div className="main-content">
          <h1 className="main-title">ODEUM</h1>
          <p className="sub-title">Discover your music personality</p>
          <Link to="/questionnaire" className="cta-button">
            Take Free Music Personality Test
          </Link>
          <Link to="/Signup" className="cta-button">
            Sign Up Now
          </Link>
        </div>
      </div>
    </div>
  );
}