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
      navigate("/");
    })
    .catch(function (error) {
      console.log(error, 'error');
      if (error.response) {
        if (error.response.status === 401) {
          alert("Invalid credentials");
        } else if (error.response.status === 400) {
          alert("Bad request. Please check the data you've entered.");
        } else if (error.response.status === 409) {
          alert("Email already exists.");
        }
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