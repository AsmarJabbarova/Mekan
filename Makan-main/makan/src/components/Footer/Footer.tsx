import { FaEnvelope, FaFacebook, FaInstagram, FaLinkedin, FaPaperPlane, FaPhone } from 'react-icons/fa'
import './Footer.css'
import { FaArrowRight, FaLocationDot, FaXTwitter} from 'react-icons/fa6'


function Footer() {
    return (
        <>
            <footer>
                <div className='footer-top-sec'>
                    <div className='footer-top-inner'>
                        <a href="">
                            <img src="https://gaviaspreview.com/wp/gowilds/wp-content/uploads/2023/01/icon-headphone.png" alt="" />
                        </a>
                        <div className='footer-p-sec'>
                            <a className='footer-p footer-p-lg' href="">Need any support for tour & travels ?</a>
                        </div>
                        <div className='arrow-sec green'>
                            <a href="">
                                <FaArrowRight className='arrow-icon'/>
                            </a>
                        </div>
                    </div>
                    <div className='footer-top-inner'>
                        <a href="">
                            <img src="https://gaviaspreview.com/wp/gowilds/wp-content/uploads/2023/01/icon-travel.png" alt="" />
                        </a>
                        <div className='footer-p-sec'>
                            <a className='footer-p footer-p-lg' href="">Ready to Get Started With Vacations!</a>
                        </div>
                        <div className='arrow-sec orange'>
                            <a href="">
                                <FaArrowRight className='arrow-icon'/>
                            </a>
                        </div>
                    </div>
                </div>
                <div className='line'></div>
                <div className='footer-bottom-sec'>
                    <div className='footer-bottom-about footer-bottom-inner'>
                        <h1>Məkan</h1>
                        <p>To take trivial example which us
                        ever undertakes laborious physica exercise except obsome.</p>
                        <div className='bottom-socials'>
                            <button className='social-btn'>
                                <a href="">
                                    <FaXTwitter className='social-btn-icon'/>
                                </a>
                            </button>
                            <button className='social-btn'>
                                <a href="">
                                    <FaFacebook className='social-btn-icon'/>
                                </a>
                            </button>
                            <button className='social-btn'>
                                <a href="">
                                    <FaInstagram className='social-btn-icon'/>
                                </a>
                            </button>
                            <button className='social-btn'>
                                <a href="">
                                    <FaLinkedin className='social-btn-icon'/>
                                </a>
                            </button>
                        </div>
                    </div>
                    <div className='footer-bottom-pages footer-bottom-inner'>
                        <h1>Pages</h1>
                        <div className='footer-bottom-pages-inner'>
                            <a className='footer-p' href="">About us</a>
                            <a className='footer-p' href="">Community blog</a>
                            <a className='footer-p' href="">Work with us</a>
                            <a className='footer-p' href="">Privacy policy</a>
                            <a className='footer-p' href="">Contact us</a>
                        </div>
                    </div>
                    <div className='footer-bottom-newsletters footer-bottom-inner'>
                        <h1>Newsletter</h1>
                        <div>
                            <p>Subscribe our newsletter to get our latest update & news.</p>
                        </div>
                        <div>
                            <form action="">
                                <input type="mail" placeholder='Email Address'/>
                                <button className='send-btn' type="submit">
                                    <FaPaperPlane/>
                                </button>
                            </form>
                        </div>
                    </div>
                    <div className='footer-bottom-contact footer-bottom-inner'>
                        <h1>Contact</h1>
                        <div>
                            <div className='footer-contact-sec'>
                                <div className='contact-icon'>
                                    <FaPhone/>
                                </div>
                                <div className='contact-infos'>
                                    <p>Drop a line</p>
                                    <p>+00 (123) 456 889</p>
                                </div>
                            </div>
                            <div className='footer-contact-sec'>
                                <div className='contact-icon'>
                                        <FaEnvelope/>
                                    </div>
                                    <div className='contact-infos'>
                                        <p> Email Address</p>
                                        <p>contact@example.com</p>
                                    </div>
                                </div>
                            <div className='footer-contact-sec'>
                                <div className='contact-icon'>
                                        <FaLocationDot/>
                                    </div>
                                    <div className='contact-infos'>
                                        <p>Visit office</p>
                                        <p>583 Main Street, NY, USA</p>
                                    </div>
                                </div>
                        </div>
                    </div>
                </div>
                <div className='copyright-sec'>
                    <p>© 2024 Copyrights by Məkan. All Rights Reserved</p>
                </div>
            </footer>
        </>
    )
}

export default Footer
