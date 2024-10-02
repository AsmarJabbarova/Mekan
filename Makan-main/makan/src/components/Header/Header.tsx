import {FaCartShopping, FaEnvelope, FaFacebook, FaInstagram, FaLocationDot, FaPinterest, FaXTwitter} from 'react-icons/fa6';
import './Header.css'


function Header() {
    return (
        <>
            <section className='header-top'>
                <div className='header-top-left'>
                    <div className='header-inner'>
                        <FaLocationDot className='header-icon'/>
                        <p className='header-p'>250 Main Street, 2nd Floor, USA</p>
                    </div>
                    <div className='header-inner'>
                        <FaEnvelope className='header-icon'/>
                        <p className='header-p'>contact@example.com</p>
                    </div>
                </div>
                <div className='header-top-right'>
                    <div className='header-inner'>
                        <a className='header-p'>Booking Now</a>
                        <a className='header-p'>About</a>
                        <a>
                            <FaCartShopping/>
                        </a>
                    </div>
                    <div className='header-top-right-socials'>
                        <a> <FaFacebook/> </a>
                        <a> <FaXTwitter/> </a>
                        <a> <FaInstagram/> </a>
                        <a> <FaPinterest/> </a>
                    </div>
                </div>
            </section>
        </>
    )
}

export default Header
