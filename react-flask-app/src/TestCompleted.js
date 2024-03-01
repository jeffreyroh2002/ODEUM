import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import Header from "./components/Header";
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default function TestCompleted() {
    const location = useLocation();
    const testId = new URLSearchParams(location.search).get('testId');
    const [testResults, setTestResults] = useState(null);

    // Refs for the charts to manage instances
    const genreChartRef = useRef(null);
    const moodChartRef = useRef(null);
    const vocalChartRef = useRef(null);

    useEffect(() => {
        if (!testId) {
            console.error('Test ID is missing.');
            return;
        }

        fetch(`/test_results?testId=${testId}`)
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

    useEffect(() => {
        if (testResults) {
            initializeCharts();
        }

        // Cleanup function to destroy charts on component unmount or before reinitializing
        return () => {
            if (genreChartRef.current) {
                genreChartRef.current.destroy();
            }
            if (moodChartRef.current) {
                moodChartRef.current.destroy();
            }
            if (vocalChartRef.current) {
                vocalChartRef.current.destroy();
            }
        };
    }, [testResults]); // This useEffect depends on testResults

    const initializeCharts = () => {
        const genreCtx = document.getElementById('genreRadarChart').getContext('2d');
        const moodCtx = document.getElementById('moodRadarChart').getContext('2d');
        const vocalCtx = document.getElementById('vocalRadarChart').getContext('2d');

        // Destroy existing charts if they exist
        if (genreChartRef.current) genreChartRef.current.destroy();
        if (moodChartRef.current) moodChartRef.current.destroy();
        if (vocalChartRef.current) vocalChartRef.current.destroy();

        // Initialize new chart instances with example data and options
        genreChartRef.current = new Chart(genreCtx, {
            type: 'radar',
            data: {
                labels: Object.keys(testResults.genre_score),
                datasets: [{
                    label: 'Genre Preferences',
                    data: Object.values(testResults.genre_score),
                    fill: true,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgb(255, 99, 132)',
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(255, 99, 132)'
                }]
            },
            options: {
                elements: {
                    line: {
                        borderWidth: 3
                    }
                },
                scales: {
                    r: {
                        angleLines: {
                            display: false
                        },
                        suggestedMin: 0,
                        suggestedMax: 10
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Genre Preferences'
                    }
                }
            },
        });

        moodChartRef.current = new Chart(moodCtx, {
            type: 'radar',
            data: {
                labels: Object.keys(testResults.mood_score),
                datasets: [{
                    label: 'Mood Preferences',
                    data: Object.values(testResults.mood_score),
                    fill: true,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgb(54, 162, 235)',
                    pointBackgroundColor: 'rgb(54, 162, 235)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(54, 162, 235)'
                }]
            },
            options: {
                elements: {
                    line: {
                        borderWidth: 3
                    }
                },
                scales: {
                    r: {
                        angleLines: {
                            display: false
                        },
                        suggestedMin: 0,
                        suggestedMax: 10
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Mood Preferences'
                    }
                }
            },
        });

        vocalChartRef.current = new Chart(vocalCtx, {
            type: 'radar',
            data: {
                labels: Object.keys(testResults.vocal_score),
                datasets: [{
                    label: 'Vocal Timbre Preferences',
                    data: Object.values(testResults.vocal_score),
                    fill: true,
                    backgroundColor: 'rgba(255, 206, 86, 0.2)',
                    borderColor: 'rgb(255, 206, 86)',
                    pointBackgroundColor: 'rgb(255, 206, 86)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(255, 206, 86)'
                }]
            },
            options: {
                elements: {
                    line: {
                        borderWidth: 3
                    }
                },
                scales: {
                    r: {
                        angleLines: {
                            display: false
                        },
                        suggestedMin: 0,
                        suggestedMax: 10
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Vocal Timbre Preferences'
                    }
                }
            },
        });
    };

    // Function to render preference scales (if applicable)
    const renderPreferenceScales = (scores, title) => {
        return (
            <div>
                <h3>{title} Preferences:</h3>
                <ul>
                    {Object.entries(scores).map(([key, value]) => (
                        <li key={key}>{key}: {value}</li>
                    ))}
                </ul>
            </div>
        );
    };

    return (
        <div>
            <Header />
            <h1>Test Completed</h1>
            <p>Test ID: {testId}</p>
            {testResults && (
                <div>
                    {/* Radar charts for genre, mood, and vocal preferences */}
                    <canvas id="genreRadarChart"></canvas>
                    <canvas id="moodRadarChart"></canvas>
                    <canvas id="vocalRadarChart"></canvas>
                    {/* Displaying preference scales */}
                    {renderPreferenceScales(testResults.genre_score, "Genre")}
                    {renderPreferenceScales(testResults.mood_score, "Mood")}
                    {renderPreferenceScales(testResults.vocal_score, "Vocal")}
                    {/* Displaying messages */}
                    <div className="display-messages">
                        {testResults.display_messages && testResults.display_messages.length > 0 ? (
                            testResults.display_messages.map((message, index) => (
                                <p key={index}>{message}</p>
                            ))
                        ) : (
                            <p>There are no specific messages to display.</p>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}