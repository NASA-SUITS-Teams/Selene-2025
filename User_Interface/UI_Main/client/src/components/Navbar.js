import React from 'react';
import { NavLink } from 'react-router-dom';  // Import NavLink
import './css/NavbarCSS.css';

function Navbar() {
  return (
    <div className="navbar">
      <div className="navbar-items">
        <NavLink 
          to="/eva" 
          className={({ isActive }) => (isActive ? 'navbar-item active-link' : 'navbar-item')}
        >
          EVA
        </NavLink>
        <NavLink 
          to="/map" 
          className={({ isActive }) => (isActive ? 'navbar-item active-link' : 'navbar-item')}
        >
          Map
        </NavLink>
        <NavLink 
          to="/uia" 
          className={({ isActive }) => (isActive ? 'navbar-item active-link' : 'navbar-item')}
        >
          UIA
        </NavLink>
        <NavLink 
          to="/setup" 
          className={({ isActive }) => (isActive ? 'navbar-item active-link' : 'navbar-item')}
        >
          Setup
        </NavLink>
      </div>
      <h2 className="team-title">Team Selene</h2>
    </div>
  );
}

export default Navbar;
