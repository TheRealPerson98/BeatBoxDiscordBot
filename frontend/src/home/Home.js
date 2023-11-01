import React from 'react';

const homeStyle = {
    backgroundColor: '#001F3F',    // dark blue color
    minHeight: 'calc(100vh - 60px)', // Adjust for footer height, assuming it's 60px
    position: 'relative',
    zIndex: '5'
};

const contentStyle = {
    marginLeft: '50px'  // 50 pixels margin to the left for the content only
};

function Home() {
    return (
        <div style={homeStyle}>
            <div style={contentStyle}>
                Welcome to the Home Page!
            </div>
        </div>
    );
}

export default Home;
