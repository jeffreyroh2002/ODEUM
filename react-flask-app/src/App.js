import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Home from './Home';
import Signup from './Signup';
import Login from './Login'
import Questionnaire from './Questionnaire';
import BeforeTest from './BeforeTest';

import Database from './Database';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} exact />
        <Route path="/Signup" element={<Signup />} />
        <Route path="/Login" element={<Login />} />
        <Route path="/BeforeTest" element={<BeforeTest />} />
        <Route path="/questionnaire" element={<Questionnaire />} />
        <Route path="/Database" element={<Database />} />
      </Routes>
    </Router>
  );
}

export default App;