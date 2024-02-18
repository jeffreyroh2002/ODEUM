// Signup.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate instead of useHistory
import Header from './components/Header';
import './Login.css';

export default function Signup(){

  useEffect(() => {
    axios.get('/csrf-token').then(response => {
      setCsrfToken(response.data.csrf_token);
    });
  }, []);

  const [email,setEmail] = useState('');
  const [password,setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [csrfToken, setCsrfToken] = useState('');

  // For Routing back to prev page
  const navigate = useNavigate();

  const logInUser = () => {
    axios.post('/login', {
      email: email,
      password: password,
      remember_me: rememberMe
    }, {
      headers: {
        'X-CSRF-Token': csrfToken // Replace `csrfToken` with the actual token
      }
    })
    .then(function (response) {
      console.log(response);
      navigate(-1);
    })
    .catch(function (error) {
      console.log(error);
      if (error.response && error.response.status === 400 || error.response.status === 401) {
        alert(error.response.data.error);
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
          <h2>Log in</h2>
          <form>
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
            <button type="button" onClick={() => logInUser()} >Log in</button>
            <div className="form-group">
              <label>
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                />
                Remember Me
              </label>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};