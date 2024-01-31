import React from "react"
import logo from '../images/logo.png'

export default function Header() {
    return (
        <header className="header">
            <img 
                src={logo} alt="Logo" 
                className="header--image"
            />
        </header>
    )
}