import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css';
import axios from 'axios';
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

export default function Sidebar({ isOpen, onClose, isLoggedIn, onLogout}) {
  const BASE_URL = process.env.REACT_APP_API_BASE_URL;
  const sidebarStyle = isOpen ? "sidebar open" : "sidebar";
  const MySwal = withReactContent(Swal)

  useEffect(() => {
    axios.get(`${BASE_URL}/csrf-token`).then(response => {
      setCsrfToken(response.data.csrf_token);
    });
  }, []);

  const [csrfToken, setCsrfToken] = useState('');

  // Function to handle logout
  const handleLogout = () => {
    axios.post(`${BASE_URL}/logout`, {}, {
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
  
  function handleHomeClick() {
    MySwal.fire({
      title: "Navigating to home...",
      timer: 500,
      timerProgressBar: false,
      didOpen: () => {
        Swal.showLoading();
      }
    })
  }
  return (
    <div className={sidebarStyle}>
      <div className="sidebar-content">
        <button className="close-button" onClick={onClose}>
          Close
        </button>
        <ul>
          <li>
            <Link to="/" className="sidebar-button" onClick={handleHomeClick}>Home</Link>
          </li>
          {isLoggedIn && (
            <li>
              <Link to="/Profile" className="sidebar-button">My Profile</Link>
            </li>
          )}
          {!isLoggedIn ? (
            <>
              <li>
                <Link to="/Login" className="sidebar-button">Login</Link>
              </li>
              <li>
                <Link to="/Signup" className="sidebar-button">Sign Up</Link>
              </li>
            </>
          ) : (
            <li>
              <Link to="/" className="sidebar-button" onClick={handleLogout}>Log Out</Link>
            </li>
          )}
        </ul>
        <Link 
            to={isLoggedIn ? "/beforeTest" : "/login"} // Conditional routing based on isLoggedIn
            className="sidebar-button"
          >
            Get Free Test
        </Link>
      </div>
    </div>
  );
}