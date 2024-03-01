import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Header from "./components/Header"
import './TestCompleted.css';

export default function TestCompleted() {
    const location = useLocation();
    const testId = new URLSearchParams(location.search).get('testId');

    return (
        <div>
            <Header />
            <h1>Test Completed</h1>
            <p>Test ID: {testId}</p>
            {/* You can use the testId value as needed */}
        </div>
    );
}