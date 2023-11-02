import styled from 'styled-components';

export const Navbar = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: ${props => (props.isMenuOpen ? '15vw' : '50px')};
  background: ${props => (props.isMenuOpen ? 'rgba(0, 0, 0, 0.8)' : '#000')};
  z-index: 10;
  transition: width 0.3s, background 0.3s;
`;

export const Bar = styled.div`
  width: 35px;
  height: 3px;
  margin: 6px auto;
  background-color: #fff;
`;

export const Menu = styled.div`
  position: absolute;
  top: 50px;
  left: 0;
  background: transparent;
  width: 100%;
  display: ${props => (props.isMenuOpen ? 'flex' : 'none')};
  flex-direction: column;
  justify-content: space-between;
  height: calc(100% - 50px);
`;

export const Link = styled.a`
  display: block;
  padding: 10px 20px;
  color: #fff;
  text-decoration: none;
  transition: background-color 0.3s;
  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
`;

export const Button = styled.button`
  display: block;
  padding: 10px 20px;
  margin-top: 10px;
  background-color: #4caf50;
  color: #fff;
  border: none;
  cursor: pointer;
  align-self: center;
  margin-bottom: 15px;
  border-radius: 5px;
  transition: background-color 0.3s;
  &:hover {
    background-color: #45a049;
  }
`;