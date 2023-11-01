import React from 'react';
import footerStyle from './footerStyle';  // Importing the styles

function Footer() {
    return (
        <footer style={footerStyle.footer}>
            <div style={footerStyle.row}>
                <a style={footerStyle.link} href="#"><i className="fa fa-facebook" style={footerStyle.icon}></i></a>
                <a style={footerStyle.link} href="#"><i className="fa fa-instagram" style={footerStyle.icon}></i></a>
                <a style={footerStyle.link} href="#"><i className="fa fa-youtube" style={footerStyle.icon}></i></a>
                <a style={footerStyle.link} href="#"><i className="fa fa-twitter" style={footerStyle.icon}></i></a>
            </div>

            <div style={footerStyle.row}>
                <ul style={footerStyle.ul}>
                    <li style={footerStyle.li}><a style={footerStyle.link} href="/home">Home</a></li>
                    <li style={footerStyle.li}><a style={footerStyle.link} href="/privacy-policy">Privacy Policy</a></li>
                    <li style={footerStyle.li}><a style={footerStyle.link} href="/terms">Terms & Conditions</a></li>
                    <li style={footerStyle.li}><a style={footerStyle.link} href="/temp">Temp</a></li>
                </ul>
            </div>

            <div style={footerStyle.row}>
                INFERNO Copyright © 2021 Inferno - All rights reserved || Designed By: Person98
            </div>
        </footer>
    );
}

export default Footer;
