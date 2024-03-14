import React, {useState, useEffect} from "react"
import Header from "./components/Header"
import './BeforeTest.css';
import next_button from "./images/next_button.png"
import { useNavigate } from 'react-router-dom';

export default function App() {

    const [audioFileId, setAudioFileId] = useState('');
    const [testId, setTestId] = useState('');

    useEffect(() => {
        fetch(`/before_test_info`)
        .then(res => res.json())
        .then(data => {
            setAudioFileId(data.audio_file_id);
            setTestId(data.test_id)
        })
        .catch(error => console.error('Error fetching audio file info:', error));
    }, []); 

    useEffect(() => {
        // Action to be performed when audioFileId or testId changes
        console.log("Updated audioFileId:", audioFileId);
        console.log("Updated testId:", testId);
    }, [audioFileId, testId]);

    const navigate = useNavigate();

    const navigateToQuestionnaire = () => {
        // Hardcoded testType
        const testType = 1;
        console.log("Next audioFileId:",audioFileId)
        console.log("passing test Id:", testId)
        navigate(`/Questionnaire?audio_file_id=${1}&test_type=${testType}&test_id=${testId}`);
        // This works for now, but it fails to dynamically update based on
        // how many questions user already answered. ideally use audioFileId
        // instead of 1 but it doesn't seem to work
    };

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
            <button className="start--button" onClick={() => navigateToQuestionnaire(audioFileId, testId)}>
                <img src={next_button} alt="Next Button" />
            </button>
        </div>
    )
}