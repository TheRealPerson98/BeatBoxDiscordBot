import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import CookieUtil from '../util/CookieUtil';
import NavBarStyles from './NavBarStyles';


function NavBar() {
    const navigate = useNavigate();

    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [roles, setRoles] = useState([]);
    const isAdmin = roles.includes("Admin");
    const styles = NavBarStyles(isMenuOpen);

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
        e.stopPropagation();  // to prevent the navbar from closing when the button is clicked
        if (isAdmin) {
            navigate('/admin');
        } else {
            // If you're navigating outside your React app, then window.location.href is okay
            window.location.href = "http://localhost:5000/auth/discord";
        }
    };

    return (
        <div style={styles.navbar} onClick={handleMenuToggle}>
            <div style={styles.bar}></div>
            <div style={styles.bar}></div>
            <div style={styles.bar}></div>

            <div style={{ ...styles.menu, display: isMenuOpen ? 'flex' : 'none' }}>
                <div>
                    <a style={styles.link} href="/">Home</a>
                    <a style={styles.link} href="/privacy-policy">Privacy Policy</a>
                    <a style={styles.link} href="/terms">Terms & Conditions</a>
                    <a style={styles.link} href="/temp">Temp</a>
                </div>
                <button style={styles.button} onClick={handleButtonClick}>
                    {isAdmin ? 'Admin Panel' : 'Login'}
                </button>
            </div>
        </div>
    );
}

export default NavBar;
