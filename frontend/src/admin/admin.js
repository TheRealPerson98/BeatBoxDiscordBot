import React, { useState, useEffect } from 'react';
import { boxStyle, adminContainerStyle } from './AdminStyles';

function Admin() {
    const [members, setMembers] = useState([]);
    const [roles, setRoles] = useState([]);

    useEffect(() => {
        fetch("http://localhost:5000/members")
            .then(response => response.json())
            .then(data => setMembers(data));

        const roleCookies = document.cookie.split('; ').filter(row => row.startsWith('role_'));
        const fetchedRoles = roleCookies.map(cookie => cookie.split('=')[0].replace('role_', ''));
        if (fetchedRoles.length > 0) {
            setRoles(fetchedRoles);
            console.log(fetchedRoles);
        }
    }, []);

    const isAuthenticated = roles.includes('Admin');

    if (!isAuthenticated) {
        return <div>You do not have permission to access this page.</div>;
    }

    return (
        <div className="admin-section" style={adminContainerStyle}>
            <h2>Member Management</h2>
            <div>
                <div style={boxStyle}>Box 1</div>
                <div style={boxStyle}>Box 2</div>
                <div style={boxStyle}>Box 3</div>
            </div>
            <p>Members in the Discord Server:</p>
            <ul>
                {members.map(member => (
                    <li key={member}>{member}</li>
                ))}
            </ul>
            <p>Your roles:</p>
            <ul>
                {roles.map(role => (
                    <li key={role}>{role}</li>
                ))}
            </ul>
        </div>
    );
}

export default Admin;
