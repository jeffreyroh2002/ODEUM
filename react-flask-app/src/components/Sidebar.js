import React from "react";
import { Link } from 'react-router-dom';
import './Sidebar.css';
import axios from 'axios';

export default function Sidebar({ isOpen, onClose, isLoggedIn }) {
  const sidebarStyle = isOpen ? "sidebar open" : "sidebar";

  // Function to handle logout
  const handleLogout = () => {
    axios.get('/logout')
      .then(response => {
        // Handle successful logout, such as redirecting to another page or updating state
        console.log("Logout successful");
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