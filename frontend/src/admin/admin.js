// Admin.js
import React, { useState, useEffect } from 'react';
import AdminMenu from './utils/AdminMenu';
import { Container, MemberList, MemberCard, MemberContent, MemberInfo, Info, Roles, RolesIcon, RolesTooltip, ButtonGroup, Button } from './AdminStyles';
import { AiOutlineEye } from 'react-icons/ai';

function Admin() {
  const [message, setMessage] = useState('');
  const [members, setMembers] = useState([]);
  const [showTooltip, setShowTooltip] = useState(-1); // Added state to keep track of which tooltip is visible

  useEffect(() => {
    if (message === 'You clicked Members') {
      fetch('http://localhost:5000/members')
        .then(response => response.json())
        .then(data => {
          setMembers(data);
        })
        .catch(error => console.log('Error fetching members:', error));
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
    };

    document.addEventListener('mousedown', handleDocumentClick);

    return () => {
      document.removeEventListener('mousedown', handleDocumentClick);
    };
  }, [showTooltip]);
  const handleIconClick = (index) => { // Added function to handle icon click
    console.log("eye clicked");
    setShowTooltip(showTooltip === index ? -1 : index);
  };

  return (
    <Container>
      <AdminMenu onButtonClick={handleButtonClick} />
      <div>{message}</div>
      {message === 'You clicked Members' && (
        <MemberList>
          {members.map((member, index) => (
            <MemberCard key={index}>
              <MemberContent>
                <MemberInfo>
                  <Info>Name: {member[0]}</Info>
                  {member[1] !== null && <Info>Nickname: {member[1]}</Info>}
                  <Roles>
                    <RolesIcon onClick={() => handleIconClick(index)}>
                      <AiOutlineEye />
                    </RolesIcon>
                    <RolesTooltip className={showTooltip === index ? 'visible' : ''}>
                      {member[2]}
                    </RolesTooltip>
                  </Roles>
                </MemberInfo>
              </MemberContent>
              <ButtonGroup>
                <Button>Moderation</Button>
                <Button>Eco</Button>
                <Button>Edit</Button>
              </ButtonGroup>
            </MemberCard>
          ))}
        </MemberList>
      )}
    </Container>
  );
}

export default Admin;