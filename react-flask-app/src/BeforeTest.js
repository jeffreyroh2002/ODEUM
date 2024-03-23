import React, {useState, useEffect} from "react"
import Header from "./components/Header"
import './BeforeTest.css';
import { useNavigate } from 'react-router-dom';
import playIcon from './images/blob.png'

export default function BeforeTest() {

    const [audioFileId, setAudioFileId] = useState();
    const [testId, setTestId] = useState();

    useEffect(() => {
        fetch(`/before_test_info`)
        .then(res => res.json())
        .then(data => {
            setAudioFileId(data.audio_file_id);
            setTestId(data.test_id);
        })
        .catch(error => console.error('Error fetching audio file info:', error));
    }, []); // .

    const navigate = useNavigate()
    const navigateToQuestionnaire = () => {
        const testType = 1;
        navigate(`/Questionnaire?audio_file_id=${audioFileId}&test_type=${testType}&test_id=${testId}`)
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
                <button className="begin-test-button" onClick={() => {navigateToQuestionnaire()}}>
                    Begin!
                </button>
            </div>
        </div>
    )
}