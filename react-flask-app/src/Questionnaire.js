import React from "react"
import Header from "./components/Header"
import sample_audio from "./Audio/sample_audio.mp3"
import AudioPlayer from './components/AudioPlayer';
import Form from './components/Form';
import './Questionnaire.css';

import playIcon from './images/icons8-play-64.png'
import pauseIcon from './images/icons8-pause-64.png'

export default function App() {
    return (
        <div>
            <Header />
            <AudioPlayer 
                src={sample_audio}
                playIconPath = {playIcon}
                pauseIconPath = {pauseIcon}
            />
            <Form/>
        </div>
    )
}