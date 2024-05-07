import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import Header from "./components/Header";
import { Chart, registerables } from 'chart.js';
import './TestCompleted.css';

Chart.register(...registerables);

export default function TestCompleted() {
    const BASE_URL = process.env.REACT_APP_API_BASE_URL;
    const location = useLocation();
    const testId = new URLSearchParams(location.search).get('testId');
    const [testResults, setTestResults] = useState(null);
    const [csrfToken, setCsrfToken] = useState('');
    const [openAiResponse, setOpenAiResponse] = useState(null);

    useEffect(() => {
        axios.get(`${BASE_URL}/csrf-token`).then(response => {
          setCsrfToken(response.data.csrf_token);
        });
    }, []);

    /*
    useEffect(() => {
        axios.get(`${BASE_URL}/query_open_ai`).then(response => {
            setOpenAiResponse(response.data.open_ai_response);
        });
    }, []);
    */

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
                setTestResults(data.gpt_analysis);
            })
            .catch(error => console.error('Error fetching test results:', error));
    }, [testId]);

    return (
        <div>
            <Header />
            <h1 className="result--header">Test Completed!</h1>
            <p>{testResults}</p>
            {/* <p>{openAiResponse}</p> */}
        </div>
    );
}
