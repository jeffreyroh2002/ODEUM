// Signup.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Header from './components/Header';
import './Signup.css';

const Signup = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirm_password: ''
  });
  const [errors, setErrors] = useState({});
  const [csrfToken, setCsrfToken] = useState('');

  useEffect(() => {
    fetchCsrfToken();
  }, []);

  const fetchCsrfToken = async () => {
    try {
      const response = await axios.get('/csrf_token');
      setCsrfToken(response.data.csrf_token);
    } catch (error) {
      console.error('Failed to fetch CSRF token:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/register', formData, {
        headers: {
          'X-CSRF-TOKEN': csrfToken
        }
      });
      // Check if the response is successful
      if (response.status === 200) {
        // Redirect the user to login or display a success message
        console.log('Registration successful');
      }
    } catch (error) {
      // Handle errors from the backend
      if (error.response) {
        setErrors(error.response.data);
      } else {
        console.error('An error occurred:', error.message);
      }
    }
  };

  return (
    <div>
      <Header />
      <div className="signup-container">
        <div className="signup-form">
          <h2>Sign Up</h2>
          <form onSubmit={handleSubmit}>
            {/* Include CSRF token as a hidden input field */}
            <input type="hidden" name="_csrf" value={csrfToken} />
            <div className="form-group">
              <input
                type="text"
                placeholder="Username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <input
                type="email"
                placeholder="Email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <input
                type="password"
                placeholder="Password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <input
                type="password"
                placeholder="Confirm Password"
                name="confirm_password"
                value={formData.confirm_password}
                onChange={handleChange}
                required
              />
            </div>
            {errors && (
              <div className="error-messages">
                {errors.username && <p>{errors.username}</p>}
                {errors.email && <p>{errors.email}</p>}
                {errors.password && <p>{errors.password}</p>}
                {errors.confirm_password && <p>{errors.confirm_password}</p>}
                {/* Add error handling for other fields as needed */}
              </div>
            )}
            <button type="submit">Sign Up</button>
          </form>
          <p>
            Already have an account? <Link to="/login">Log In</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signup;