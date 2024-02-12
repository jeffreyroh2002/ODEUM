import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Home from './Home';
import Questionnaire from './Questionnaire';
import Signup from './Signup';
import Database from './Database';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} exact />
        <Route path="/questionnaire" element={<Questionnaire />} />
        <Route path="/Signup" element={<Signup />} />
        <Route path="/Database" element={<Database />} />
      </Routes>
    </Router>
  );
}

export default App;