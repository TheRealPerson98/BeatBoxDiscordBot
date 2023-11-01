
const getNavBarStyles = (isMenuOpen) => ({
        navbar: {
        position: 'fixed',
        top: '0',
        left: '0',
        height: '100%',
        width: isMenuOpen ? '15vw' : '50px', 
        background: isMenuOpen ? 'rgba(0, 0, 0, 0.8)' : '#000',
        zIndex: '10',
        transition: 'width 0.3s, background 0.3s',
    },
    bar: {
        width: '35px',
        height: '3px',
        margin: '6px auto',
        backgroundColor: '#fff',
    },
    menu: {
        position: 'absolute',
        top: '50px',
        left: '0',
        background: 'transparent',
        width: '100%',
        display: 'none',
        flexDirection: 'column',
        justifyContent: 'space-between',
        height: 'calc(100% - 50px)',
    },
    link: {
        display: 'block',
        padding: '10px 20px',
        color: '#fff',
        textDecoration: 'none',
        transition: 'background-color 0.3s',
        '&:hover': {
            backgroundColor: 'rgba(255,255,255,0.1)' // hover effect
        }
    },
    button: {
        display: 'block',
        padding: '10px 20px',
        marginTop: '10px',
        backgroundColor: '#fff',
        color: '#000',
        border: 'none',
        cursor: 'pointer',
        alignSelf: 'center',
        marginBottom: '15px' // margin from the bottom
    }
});

export default getNavBarStyles;