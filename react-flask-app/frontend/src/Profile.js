import React, { useState, useEffect } from 'react';
import Header from "./components/Header";
import { Link } from 'react-router-dom';
import './Profile.css';
import axios from 'axios';

export default function Profile() {
    const BASE_URL = process.env.REACT_APP_API_BASE_URL;
    const [userName, setUserName] = useState('');
    const [testsData, setTestsData] = useState([]);

    useEffect(() => {
        // Fetch isLoggedIn status from backend when component mounts
        axios.get(`${BASE_URL}/get_user_info`)
        .then(response => {
            setUserName(response.data.user_name);
            setTestsData(response.data.tests_data)
        })
        .catch(error => {
            console.error('Error fetching get_user_info status:', error);
        });
    }, []);

    return (
        <div>
            <Header />
            <div className="home-container">
                <div className="main-content">
                    <p className="sub-title">Welcome back, {userName}</p>
                </div>
                <div>
                    {testsData.length > 0 ? (
                        testsData.map(test => (
                            <Link key={test.id} to={`/TestCompleted?testId=${test.id}`} className="test-link">
                                <div className="test-card">
                                    <p>ID: {test.id}</p>
                                    <p>Type: {test.test_type}</p>
                                    <p>Start Time: {test.test_start_time}</p>
                                    {/* Add more fields as needed */}
                                </div>
                            </Link>
                        ))
                    ) : (
                        <p>No tests taken yet!</p>
                    )}
                </div>
            </div>
        </div>
    );
}