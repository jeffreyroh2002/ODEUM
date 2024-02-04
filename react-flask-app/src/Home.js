import React from 'react';
import Header from "./components/Header"
import { Link } from 'react-router-dom';
import './Home.css';


export default function Home() {
  return (
    <div>
      < Header /> 
      <h1>Welcome to Musicality!</h1>
      <Link to="/questionnaire">Go to Questionnaire</Link>
    </div>
  );
}