// Signup.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate instead of useHistory
import Header from './components/Header';
import './Signup.css';

export default function Signup(){

  useEffect(() => {
    axios.get('/csrf-token').then(response => {
      setCsrfToken(response.data.csrf_token);
    });
  }, []);

  const [firstName,setFirstName] = useState('');
  const [email,setEmail] = useState('');
  const [password,setPassword] = useState('');
  const [confirmPassword,setConfirmPassword] = useState('');
  const [csrfToken, setCsrfToken] = useState('');

  const navigate = useNavigate();

  const registerUser = () => {
    axios.post('/signup', {
      first_name: firstName,
      email: email,
      password: password,
      confirm_password: confirmPassword
    }, {
      headers: {
        'X-CSRF-Token': csrfToken // Replace `csrfToken` with the actual token
      }
    })
    .then(function (response) {
      console.log(response);
      navigate("/");
    })
    .catch(function (error) {
      console.log(error); // Log the error to see its structure
      if (error.response && error.response.status === 400) {
        alert(error.response.data.error); // Alert the error message from the response
      } else if (error.response && error.response.status === 401) {
        alert("Invalid credentials");
      } else if (error.response && error.response.status === 409) {
        alert("Email already exists.");
      } else {
        alert("An unexpected error occurred. Please try again later."); // Handle other errors
      }
    });
  }

  return (
    <div>
      <Header />
      <div className="signup-container">
        <div className="signup-form">
          <h2>Sign Up</h2>
          <form>
            <div className="form-group">
              <input
                type="text"
                placeholder="First Name"
                name="firstName"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <input
                type="email"
                placeholder="Email"
                name="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <input
                type="password"
                placeholder="Password"
                name="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <input
                type="password"
                placeholder="Confirm Password"
                name="confirm password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
            <button type="button" onClick={() => registerUser()} >Sign Up</button>
          </form>
          <p>
            Already have an account? <Link to="/login">Log In</Link>
          </p>
        </div>
      </div>
    </div>
  );
};