import styled from 'styled-components';


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
  color: #FFFFFF;
`;

export const Info = styled.p`
  margin: 0;
  white-space: nowrap;
`;

export const Roles = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`;

export const RolesIconContainer = styled.div`
  position: relative;
  display: flex;
  align-items: center;
`;

export const RolesIcon = styled.div`
  cursor: pointer;
`;

export const RolesTooltip = styled.div`
  position: absolute;
  background-color: #4A4A4A;
  color: #FFFFFF;
  padding: 10px;
  border-radius: 5px;
  top: 25px;
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
export const StatusDot = styled.div`
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: ${(props) =>
    props.status === 'online' ? 'green' : 'gray'};
  margin-right: 5px;
`;
export const MemberList = styled.div`
  display: flex;
  flex-direction: column;
  margin-left: 285px;
  gap: 20px;
`;
export const Dropdown = styled.div`
  display: ${(props) => (props.isOpen ? 'block' : 'none')};
  position: absolute;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  z-index: 1;
`;
export const DropdownButton = styled.button`
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  margin: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;

  &:hover {
    background-color: #45a049;
  }
`;
