import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Header.css';
import axios from 'axios';
import fret_logo from '../images/fret_logo.png'
import account_icon from '../images/account_icon.png'
import menu_icon from '../images/menu_white_24px.png'

import Sidebar from './Sidebar';

export default function Header() {

    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        // Fetch isLoggedIn status from backend when component mounts
        axios.get('/isLoggedIn')
        .then(response => {
            setIsLoggedIn(response.data.isLoggedIn);
        })
        .catch(error => {
            console.error('Error fetching isLoggedIn status:', error);
        });
    }, []);

    const [isSidebarOpen, setSidebarOpen] = React.useState(false);

    const toggleSidebar = () => {
        setSidebarOpen(!isSidebarOpen);
    };

    return (
        <header className="header">
            <Link to="/">
            <img 
                src={fret_logo} 
                alt="ODEUM" 
                className="header--image"
            />
            </Link>
            <img
                src={account_icon} 
                alt="account"
                className="header--account--image"
                onClick={toggleSidebar}
            />
            <Sidebar isOpen={isSidebarOpen} onClose={toggleSidebar} isLoggedIn={isLoggedIn}/>
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