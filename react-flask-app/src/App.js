import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import Signup from './Signup';
import Login from './Login'
import Profile from './Profile';
import Questionnaire from './Questionnaire';
import BeforeTest from './BeforeTest';
import TestCompleted from './TestCompleted';
import ArtistSelector from './ArtistSelector';
import Presurvey from './Presurvey';

import Database from './Database';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} exact />
        <Route path="/Signup" element={<Signup />} />
        <Route path="/Login" element={<Login />} />
        <Route path="/Profile" element={<Profile />} />
        <Route path="/BeforeTest" element={<BeforeTest />} />
        <Route path="/ArtistSelector" element={<ArtistSelector />} />
        <Route path="/Presurvey" element={<Presurvey />} />
        <Route path="/questionnaire" element={<Questionnaire />} />
        <Route path="/TestCompleted" element={<TestCompleted />} />
        <Route path="/Database" element={<Database />} />
      </Routes>
    </Router>
  );
}

export default App;