import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';
import Vector from '../images/Vector.png'
import account_icon from '../images/account_icon.png'

import Sidebar from './Sidebar';

export default function Header({ isLoggedIn, onLogout }) {

    const [isSidebarOpen, setSidebarOpen] = React.useState(false);

    const toggleSidebar = () => {
        setSidebarOpen(!isSidebarOpen);
    };

    const closeSidebar = () => {
        setSidebarOpen(false);
    };

    const handleLogout = () => {
        onLogout(); // Call the onLogout function passed from the parent component
        closeSidebar(); // Close the sidebar after logout
      };


    return (
        <header className="header">
            <Link to="/">
            <img 
                src={Vector} 
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
            <Sidebar 
                isOpen={isSidebarOpen} 
                onClose={toggleSidebar} 
                isLoggedIn={isLoggedIn}
                onLogout={handleLogout}
                />
        </header>
    );
}