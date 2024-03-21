import React, {useState, useEffect} from "react"
import Header from "./components/Header"
import './BeforeTest.css';
import { useNavigate } from 'react-router-dom';
import playIcon from './images/blob.png'

export default function App() {

    const [audioFileId, setAudioFileId] = useState('');
    const [testId, setTestId] = useState('');

    useEffect(() => {
        fetch(`/before_test_info`)
        .then(res => res.json())
        .then(data => {
            console.log("asdfasdf");
            setAudioFileId(data.audio_file_id);
            setTestId(data.test_id)
        })
        .catch(error => console.error('Error fetching audio file info:', error));
    }, []); 

    const navigate = useNavigate();

    const navigateToQuestionnaire = () => {
        // Hardcoded testType
        const testType = 1;
        console.log("Next audioFileId:",audioFileId)
        console.log("passing test Id:", testId)
        navigate(`/Questionnaire?audio_file_id=${audioFileId}&test_type=${testType}&test_id=${testId}`);
        // This works for now, but it fails to dynamically update based on
        // how many questions user already answered. ideally use audioFileId
        // instead of 1 but it doesn't seem to work
    };

    return (
        <div>
            <Header />
            <div className="before-test-container">
                <h1 className="before-test-title">Before Test</h1>
                <ul className="instruction--container">
                    <li className="before-test-span">
                        Answer as many questions as possible.
                    </li>
                    <li className="before-test-span">
                        Click on <img src={playIcon} width="50px" height="50px"/> to play/pause music.
                    </li>
                    <li className="before-test-span">
                        Try your best.
                    </li>
                    <li className="before-test-span">
                        Enjoy the Experience.
                    </li>
                </ul>
                <button className="begin-test-button" onClick={() => navigateToQuestionnaire(audioFileId, testId)}>
                    Begin!
                </button>
            </div>
        </div>
    )
}