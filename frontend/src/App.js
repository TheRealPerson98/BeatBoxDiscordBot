import React from 'react';
import Footer from './footer/Footer';
import Home from './home/Home';  // Import the Home component
import NavBar from './navbar/NavBar';
import Admin from './admin/admin';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

const appStyle = {
    background: '#f0f0f0',
    minHeight: '100vh',
};

function App() {
    return (
        <Router>
            <div className="App" style={appStyle}>
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
