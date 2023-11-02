import React from 'react';
import Footer from './footer/Footer';
import Home from './home/Home';  // Import the Home component
import NavBar from './navbar/NavBar';
import Admin from './admin/admin';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { createGlobalStyle } from 'styled-components';

const appStyle = {
    minHeight: '100vh',
};
const GlobalStyle = createGlobalStyle`
  body {
    background-color: #2B2B2B;
    margin: 0;
    font-family: 'Lato', sans-serif;
  }
  /* Custom scrollbar styles */
  ::-webkit-scrollbar {
    width: 10px;
  }
  ::-webkit-scrollbar-track {
    background: #1a1a1a;
  }
  ::-webkit-scrollbar-thumb {
    background: #333;
    border-radius: 5px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: #555;
  }
  scrollbar-color: #333 #1a1a1a;
  scrollbar-width: thin;
`;
function App() {
    return (
        <Router>
            <div className="App" style={appStyle}>
            <GlobalStyle />
                <NavBar />

                <Routes>
                    <Route path="/" element={<Home />} />  {/* Set Home component to the root path */}
                    <Route path="/admin" element={<Admin />} />
                </Routes>

                <Footer />
            </div>
        </Router>
    );
}

export default App;
