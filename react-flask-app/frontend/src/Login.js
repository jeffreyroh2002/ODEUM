import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate instead of useHistory
import Header from './components/Header';
import './Login.css';
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

export default function Signup(){
  const BASE_URL = process.env.REACT_APP_API_BASE_URL;
  useEffect(() => {
    axios.get(`${BASE_URL}/csrf-token`).then(response => {
      setCsrfToken(response.data.csrf_token);
    });
  }, []);

  const [email,setEmail] = useState('');
  const [password,setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [csrfToken, setCsrfToken] = useState('');
  const MySwal = withReactContent(Swal);

  // For Routing back to prev page
  const navigate = useNavigate();

  const logInUser = () => {
    axios.post(`${BASE_URL}/login`, {
      email: email,
      password: password,
      remember_me: rememberMe
    }, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': csrfToken
      }
    })
    .then(function (response) {
      console.log(response);
      if (response.data['error']) {
        MySwal.fire({
          title: response.data['error'],
          showConfirmButton: false,
          showDenyButton: false,
          showCancelButton: true,
          cancelButtonText: `OK`
        })
      }
      else navigate('/');
    })
    .catch((error) => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
        alert("Error: " + error.response.data.message);
      } else if (error.request) {
        // The request was made but no response was received
        console.log(error.request);
        alert("Error: No response from server.");
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log('Error', error.message);
        alert("Error: " + error.message);
      }
    });
  };

  return (
    <div>
      <Header />
      <div className="signup-container">
        <div className="signup-form">
          <h2>Log in</h2>
          <form>
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
            <div className="remember-me-text">
              <label>
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                />
                Remember Me
              </label>
            </div>
            <button type="button" onClick={() => logInUser()} >Login</button>
            <div className="signup-link">
              <p>Don't have an account?</p>
              <Link to="/signup">Sign Up Now</Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};