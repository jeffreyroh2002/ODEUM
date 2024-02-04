import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div>
      <h1>Home Page</h1>
      <Link to="/questionnaire">Go to Questionnaire</Link>
    </div>
  );
}