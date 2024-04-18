import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate instead of useHistory
import Header from './components/Header';
import './Signup.css';
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

export default function Signup(){
  const BASE_URL = process.env.REACT_APP_API_BASE_URL;
  
  useEffect(() => {
    axios.get(`${BASE_URL}/csrf-token`).then(response => {
      setCsrfToken(response.data.csrf_token);
    });
  }, []);

  const [firstName,setFirstName] = useState('');
  const [email,setEmail] = useState('');
  const [password,setPassword] = useState('');
  const [confirmPassword,setConfirmPassword] = useState('');
  const [csrfToken, setCsrfToken] = useState('');

  const navigate = useNavigate();
  const MySwal = withReactContent(Swal);

  const registerUser = () => {
    axios.post(`${BASE_URL}/signup`, {
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
      console.log(response)
      if (response.data['error']) {
        MySwal.fire({
          title: response.data['error'],
          showConfirmButton: false,
          showDenyButton: false,
          showCancelButton: true,
          cancelButtonText: `OK`
        })
      }
      else if (response.data['id']) navigate("/Login");
    })
    .catch((error) => alert("An unexpected error occurred. Please try again later."))
  };

  
  return (
    <div>
      <Header />
      <div className="signup-container">
        <div className="signup-form">
          <h2>Sign Up</h2>
          <form>
            <div className="form-group">
              <label htmlFor="firstname">First Name</label>
              <input
                type="text"
                name="firstName"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                name="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                name="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="confirm password">Confirm Password</label>
              <input
                type="password"
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