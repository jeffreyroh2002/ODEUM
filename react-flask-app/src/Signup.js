// Signup.js

import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate instead of useHistory
import Header from './components/Header';
import './Signup.css';

export default function Signup(){
  const [firstName,setFirstName] = useState('');
  const [email,setEmail] = useState('');
  const [password,setPassword] = useState('');

  const navigate = useNavigate();

  const registerUser = () => {
    axios.post('/signup', {
      first_name: firstName,
      email: email,
      password: password
    })
    .then(function (response) {
      console.log(response);
      navigate("/");
    })
    .catch(function (error) {
      console.log(error, 'error');
      if (error.response.status === 401) {
          alert("Invalid credentials");
      }
    });
  }

/* 
const Signup = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirm_password: ''
  });
  const [errors, setErrors] = useState({});
  const navigate = useNavigate(); // Use useNavigate hook for redirection

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/users/register', formData);
      if (response.status === 201) {
        console.log('Registration successful');
        navigate('/login'); // Redirect user to login page upon successful registration
      }
    } catch (error) {
      if (error.response && error.response.data) {
        // Backend will send back a JSON response with errors, handle them here
        setErrors(error.response.data.error || error.response.data);
      } else {
        console.error('An error occurred:', error.message);
      }
    }
  };

*/

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
            {/*   COMMENT OUT PASSWORD CONFIRMATION
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
            */}
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