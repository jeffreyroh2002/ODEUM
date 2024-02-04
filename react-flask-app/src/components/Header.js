import React from "react"
import { Link } from 'react-router-dom';
import './Header.css';

import logo from '../images/logo.png'
import account_icon from '../images/account_circle_filled_white_24px.png'
import menu_icon from '../images/menu_white_24px.png'


export default function Header() {
    return (
        <header className="header">
            <img 
                src={logo} alt="ODEUM" 
                className="header--image"
                Link to="/"
            />
            <img
                src={account_icon} alt="account"
                className="header--account--image"
            />
            <img 
                src={menu_icon} alt="menu"
                className="header--menu--image"
            />
        </header>
    );
}

/* Nav items for later
                <div className="nav-items">
                    <Link to="/about" className="nav-link">About</Link>
                    <Link to="/services" className="nav-link">Services</Link>
                    <Link to="/contact" className="nav-link">Contact</Link>
                </div>
*/

/*  OLD HEADER
        <header className="header">
            <img 
                src={logo} alt="ODEUM" 
                className="header--image"
                Link to="/"
            />
            <img
                src={account_icon} alt="account"
                className="header--account--image"
            />
            <img 
                src={menu_icon} alt="menu"
                className="header--menu--image"
            />
        </header>
*/