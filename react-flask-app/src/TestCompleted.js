import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import Header from "./components/Header";
import { Chart, registerables } from 'chart.js';
import './TestCompleted.css';

Chart.register(...registerables);

export default function TestCompleted() {
    const location = useLocation();
    const testId = new URLSearchParams(location.search).get('testId');
    const [testResults, setTestResults] = useState(null);
    /*
    useEffect(() => {
        if (!testId) {
            console.error('Test ID is missing.');
            return;
        }
        console.log("test id: ", testId);
        fetch(`/test_results?testId=${testId}`) // Adjust this URL for your backend
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                setTestResults(data);
            })
            .catch(error => console.error('Error fetching test results:', error));
    }, [testId]);
    */

    return (
        <div>
            <Header />
            <h1 className="result--header">Test Completed!</h1>
            <h2 className="result--subheader">Results Feature Coming Soon...</h2>
            {/* 
            <p>Test ID: {testId}</p>
            <p>testResults{testResults}</p>
            */}
        </div>
    );
}
