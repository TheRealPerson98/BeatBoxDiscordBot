import React, { useState } from 'react';
import {
  MemberList as StyledMemberList,
  MemberCard,
  MemberContent,
  MemberInfo,
  Info,
  Roles,
  ButtonGroup,
  Button,
  Dropdown,
  DropdownButton,
  StatusDot,
  RolesIconContainer,
  RolesIcon,
  RolesTooltip,
  
} from './MemberListStyle';
import { AiOutlineEye, AiOutlineInfoCircle } from 'react-icons/ai';

function MemberList({ members, setMembers, handleIconClick, handleInfoIconClick, showTooltip, showInfoTooltip }) {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [openDropdownUserId, setOpenDropdownUserId] = useState(null);

  const handleBanClick = (memberId) => {
    console.log("Sending user ID to server:", memberId.toString());  // Log the user ID
    fetch('http://localhost:5000/ban', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: memberId.toString(),  // Convert the user ID to string
        reason: 'Some reason',  // Optional reason for the ban
      }),
    })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data.status === "success") {
        // Remove the banned member from the members state
        setMembers(members.filter(member => member[0] !== memberId));
      }
    })
    .catch((error) => {
      console.log('Error banning member:', error);
    });
};


  const handleModerationClick = (userId) => {
    setOpenDropdownUserId((prevUserId) => (prevUserId === userId ? null : userId));
  };
  return (
    <StyledMemberList>
      {members.map((member, index) => (
        <MemberCard key={index}>
          <MemberContent>
            <MemberInfo>
              <StatusDot status={member[4]} />
              <Info><span title={`ID: ${member[0]}`}>Name: {member[1]}</span></Info>
              {member[2] !== null && <Info>Nickname: {member[2]}</Info>}
                <Roles>
                <Info>Main Role: {member[7]}</Info>
                <RolesIconContainer>
                    <RolesIcon onClick={() => handleIconClick(index)}>
                    <AiOutlineEye />
                    </RolesIcon>
                    <RolesTooltip className={showTooltip === index ? 'visible' : ''}>
                    Roles: {member[3]}
                    </RolesTooltip>
                </RolesIconContainer>
                <RolesIconContainer>
                    <RolesIcon onClick={() => handleInfoIconClick(index)}>
                    <AiOutlineInfoCircle />
                    </RolesIcon>
                    <RolesTooltip className={`info-tooltip-container ${showInfoTooltip === index ? 'visible' : ''}`}>
                    <div>Joined At: {new Date(member[5]).toLocaleDateString()}</div>
                    <div>Created At: {new Date(member[6]).toLocaleDateString()}</div>
                    </RolesTooltip>
                </RolesIconContainer>
                </Roles>

            </MemberInfo>
          </MemberContent>
          <ButtonGroup>
            <Button onClick={() => handleModerationClick(member[0])}>Moderation</Button>
            <Dropdown isOpen={openDropdownUserId === member[0]}>
              <DropdownButton onClick={() => handleBanClick(member[0])}>Ban</DropdownButton>
            </Dropdown>
            <Button>Eco</Button>
            <Button>Edit</Button>
          </ButtonGroup>
        </MemberCard>
      ))}
    </StyledMemberList>
  );
}
export default MemberList;
