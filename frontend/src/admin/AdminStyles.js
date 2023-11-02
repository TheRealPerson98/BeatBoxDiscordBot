// AdminStyles.js
import styled from 'styled-components';

export const Container = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #2C2C2C; // Dark gray background
`;

export const MemberList = styled.div`
  display: flex;
  flex-direction: column;
  margin-left: 285px;
  gap: 20px;
`;

export const MemberCard = styled.div`
  background-color: #3D3D3D; // Dark gray background
  border-radius: 10px;
  padding: 20px;
  width: 97.5%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70%; // Adjusted height
`;

export const MemberContent = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
`;

export const MemberInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
  color: #FFFFFF; // White text color
`;

export const Info = styled.p`
  margin: 0;
`;

export const Roles = styled.div`
  position: relative;
`;

export const RolesIcon = styled.div`
  display: flex;
  align-items: center;
  cursor: pointer;
`;

export const RolesTooltip = styled.div`
  position: absolute;
  background-color: #4A4A4A; // Dark gray background
  color: #FFFFFF; // White text color
  padding: 10px;
  border-radius: 5px;
  top: 30px;
  left: 0;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;

  &.visible {
    opacity: 1;
    visibility: visible;
  }
`;

export const ButtonGroup = styled.div`
  display: flex;
  gap: 10px;
  margin-top: 20px;
`;

export const Button = styled.button`
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  color: white;
  background-color: #6C3483; // Purple background color
  cursor: pointer;

  &:hover {
    background-color: #5B2C6F; // Darker purple background color
  }
`;
