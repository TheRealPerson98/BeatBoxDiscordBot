// Admin.js
import React, { useState, useEffect } from 'react';
import AdminMenu from './utils/AdminMenu';
import {
  Container,
} from './AdminStyles';

import MemberList from './utils/memberlist/MemberList';  // <-- Import MemberList

function Admin() {
  const [message, setMessage] = useState('');
  const [members, setMembers] = useState([]);
  const [showTooltip, setShowTooltip] = useState(-1);
  const [showInfoTooltip, setShowInfoTooltip] = useState(-1);

  useEffect(() => {
    if (message === 'You clicked Members') {
      fetch('http://localhost:5000/members')
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          setMembers(data);
        })
        .catch((error) => console.log('Error fetching members:', error));
    }
  }, [message]);

  const handleButtonClick = (buttonName) => {
    setMessage(`You clicked ${buttonName}`);
  };

  useEffect(() => {
    const handleDocumentClick = (event) => {
      if (showTooltip !== -1 && event.target.closest('.tooltip-container') === null) {
        setShowTooltip(-1);
      }
      if (showInfoTooltip !== -1 && event.target.closest('.info-tooltip-container') === null) {
        setShowInfoTooltip(-1);
      }
    };

    document.addEventListener('mousedown', handleDocumentClick);

    return () => {
      document.removeEventListener('mousedown', handleDocumentClick);
    };
  }, [showTooltip, showInfoTooltip]);

  const handleIconClick = (index) => {
    setShowTooltip(showTooltip === index ? -1 : index);
  };

  const handleInfoIconClick = (index) => {
    setShowInfoTooltip(showInfoTooltip === index ? -1 : index);
  };

return (
    <Container>
      <AdminMenu onButtonClick={handleButtonClick} />
      <div>{message}</div>
      {message === 'You clicked Members' && (
        <MemberList
          members={members}
          setMembers={setMembers}
          handleIconClick={handleIconClick}
          handleInfoIconClick={handleInfoIconClick}
          showTooltip={showTooltip}
          showInfoTooltip={showInfoTooltip}
        />
      )}
    </Container>
  );
  
}

export default Admin;