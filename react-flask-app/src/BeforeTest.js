import React from "react"
import Header from "./components/Header"
import './BeforeTest.css';
import next_button from "./images/next_button.png"
import { useNavigate } from 'react-router-dom';

export default function App() {

    const navigate = useNavigate();

    function handleNextButton(){
        navigate('/Questionnaire'); // Navigate to /Questionnaire route
    }

    return (
        <div>
            <Header />
            <h1>Before Test</h1>
            <ul>
                <li className="before-test-span">
                    음악을 듣고 질문에 답이 되는 선택지를 클릭하세요.<br/>
                </li>
                <span className="before-test-span">
                    <br/>
                </span>
                <li className="before-test-span">
                    곡의 전체적인 느낌을 묻는 질문은 필수로 답해야 합니다.<br/>
                </li>
                <span className="before-test-span">
                    <br/>
                </span>
                <li className="before-test-span">
                    추가 질문은 해도 되고 안해도 됩니다.<br/>
                </li>
                <span className="before-test-span">
                    <br/>
                </span>
                <li className="before-test-span">
                    가능한 추가질문에 답해주는 것이 도움이 됩니다.
                </li>
            </ul>
            <button className="next--button" onClick={handleNextButton}>
                <img src={next_button} alt="Next Button" />
            </button>
        </div>
    )
}