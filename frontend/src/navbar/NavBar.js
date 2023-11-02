// NavBar.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import CookieUtil from '../util/CookieUtil';
import { Navbar, Bar, Menu, Link, Button } from './NavBarStyles';

function NavBar() {
  const navigate = useNavigate();

  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [roles, setRoles] = useState([]);
  const isAdmin = roles.includes('Admin');

  useEffect(() => {
    const fetchedRoles = CookieUtil.fetchRolesFromCookies();
    if (fetchedRoles.length > 0) {
      setRoles(fetchedRoles);
    }
  }, []);

  const handleMenuToggle = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleButtonClick = (e) => {
    e.stopPropagation();
    setIsMenuOpen(false); // close the nav bar
    if (isAdmin) {
      navigate('/admin');
    } else {
      window.location.href = 'http://localhost:5000/auth/discord';
    }
  };

  return (
    <Navbar isMenuOpen={isMenuOpen} onClick={handleMenuToggle}>
      <Bar />
      <Bar />
      <Bar />
      <Menu isMenuOpen={isMenuOpen}>
        <div>
          <Link href="/">Home</Link>
          <Link href="/privacy-policy">Privacy Policy</Link>
          <Link href="/terms">Terms & Conditions</Link>
          <Link href="/temp">Temp</Link>
        </div>
        <Button onClick={handleButtonClick}>{isAdmin ? 'Admin Panel' : 'Login'}</Button>
      </Menu>
    </Navbar>
  );
}

export default NavBar;
