import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css';
import axios from 'axios';

export default function Sidebar({ isOpen, onClose, isLoggedIn, onLogout}) {
  
  const sidebarStyle = isOpen ? "sidebar open" : "sidebar";
  
  useEffect(() => {
    axios.get('/csrf-token').then(response => {
      setCsrfToken(response.data.csrf_token);
    });
  }, []);

  const [csrfToken, setCsrfToken] = useState('');

  // Function to handle logout
  const handleLogout = () => {
    axios.post('/logout', {}, {
      headers: {
        'X-CSRF-TOKEN': csrfToken
      }
    })
      .then(response => {
        // Handle successful logout, such as redirecting to another page or updating state
        console.log("Logout successful");
        onLogout(); // Notify the parent component about logout
        onClose();
      })
      .catch(error => {
        // Handle error if logout fails
        console.error("Logout failed:", error);
      });
  };
  
  return (
    <div className={sidebarStyle}>
      <div className="sidebar-content">
        <button className="close-button" onClick={onClose}>
          Close
        </button>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          {isLoggedIn && (
            <li>
              <Link to="/Profile">My Profile</Link>
            </li>
          )}
          {!isLoggedIn ? (
            <li>
              <Link to="/login">Sign Up</Link>
            </li>
          ) : (
            <li>
              <Link to="/" onClick={handleLogout}>Log Out</Link>
            </li>
          )}
        </ul>
        <Link 
            to={isLoggedIn ? "/beforeTest" : "/login"} // Conditional routing based on isLoggedIn
            className="cta-button"
          >
            Get Free Test
        </Link>
      </div>
    </div>
  );
}