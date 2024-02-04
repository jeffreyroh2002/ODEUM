import React from "react";
import { Link } from 'react-router-dom';
import './Sidebar.css';
export default function Sidebar({ isOpen, onClose }) {
  const sidebarStyle = isOpen ? "sidebar open" : "sidebar";

  return (
    <div className={sidebarStyle}>
      <div className="sidebar-content">
        <button className="close-button" onClick={onClose}>
          Close
        </button>
        <ul>
          <li>
            <Link to="/login">Log in / Sign up</Link>
          </li>
          <li>
            <Link to="/profile">My Profile</Link>
          </li>
          <li>
            <Link to="/help">Help Center</Link>
          </li>
        </ul>
        <Link to="/questionnaire" className="cta-button">
          Get Free Test
        </Link>
      </div>
    </div>
  );
}
