// AdminMenu.js
import React from 'react';
import styled from 'styled-components';

const MenuContainer = styled.div`
  position: fixed;
  top: 0;
  left: 25px;
  width: 250px;
  height: 100vh;
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: stretch;
  padding: 0;
`;

const FancyButton = styled.button`
  background-color: #34495e;
  color: #ecf0f1;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 0;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  &:hover {
    background-color: #2c3e50;
    color: #bdc3c7;
  }
  width: 100%;
  border-bottom: 1px solid #2c3e50;
`;

function AdminMenu({ onButtonClick }) {
  return (
    <MenuContainer>
      <FancyButton onClick={() => onButtonClick('Members')}>Members</FancyButton>
      <FancyButton>Events</FancyButton>
      <FancyButton>Eco</FancyButton>
      <FancyButton>Moderation</FancyButton>
      <FancyButton style={{ borderBottom: 'none' }}>Config</FancyButton>
    </MenuContainer>
  );
}

export default AdminMenu;