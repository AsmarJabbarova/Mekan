import { FaEnvelope, FaFacebook, FaInstagram, FaLinkedin, FaPaperPlane, FaPhone } from 'react-icons/fa'
import './FooterStyles.css'
import { FaArrowRight, FaLocationDot, FaXTwitter} from 'react-icons/fa6'
import { Field, Form, Formik } from 'formik'
import * as Yup from 'yup';

interface FormValues {
    email: string;
  }
  
  const initialValues: FormValues = {
    email: ''
  };
  
  const validationSchema = Yup.object({
    email: Yup.string()
      .email('Invalid email format')
      .required('Email is required'),
  });

function Footer() {
    const onSubmit = (values: FormValues) => {
    console.log('Form data', values);
  };
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
                                <a href='https://www.x.com/' target="_blank">
                                    <FaXTwitter className='social-btn-icon'/>
                                </a>
                            </button>
                            <button className='social-btn'>
                                <a href='https://www.facebook.com/' target="_blank">
                                    <FaFacebook className='social-btn-icon'/>
                                </a>
                            </button>
                            <button className='social-btn'>
                                <a href='https://www.instagram.com/' target="_blank">
                                    <FaInstagram className='social-btn-icon'/>
                                </a>
                            </button>
                            <button className='social-btn'>
                                <a href="https://www.linkedin.com/" target="_blank">
                                    <FaLinkedin className='social-btn-icon'/>
                                </a>
                            </button>
                        </div>
                    </div>
                    <div className='footer-bottom-pages footer-bottom-inner'>
                        <h1>Pages</h1>
                        <div className='footer-bottom-pages-inner'>
                            <a className='footer-p' href="/about">About us</a>
                            <a className='footer-p' href="/about">Community blog</a>
                            <a className='footer-p' href="/about">Privacy policy</a>
                            <a className='footer-p' href="/contact">Contact us</a>
                        </div>
                    </div>
                    <div className='footer-bottom-newsletters footer-bottom-inner'>
                        <h1>Newsletter</h1>
                        <div>
                            <p>Subscribe our newsletter to get our latest update & news.</p>
                        </div>
                        <div>
                            <Formik
                                initialValues={initialValues}
                                validationSchema={validationSchema}
                                onSubmit={onSubmit}
                                validateOnBlur={false} // Disable validation on blur
                                validateOnChange={false} // Disable validation on change
                                >
                                <Form className='form-footer'>
                                    <Field type="mail" id="mail" name="mail" className="footer-contact-input" placeholder='Email Address'/>
                                    <button className='send-btn' type="submit">
                                        <FaPaperPlane/>
                                    </button>
                                </Form>
                            </Formik>
                        </div>
                    </div>
                    <div className='footer-bottom-contact footer-bottom-inner'>
                        <h1>Contact</h1>
                        <div>
                            <div className='footer-contact-sec'>
                                <div className='contact-icon'>
                                    <FaPhone color='#63ab45'/>
                                </div>
                                <div className='contact-infos'>
                                    <p className='contact-info-header'>Drop a line</p>
                                    <p className='contact-info-body'>+00 (123) 456 889</p>
                                </div>
                            </div>
                            <div className='footer-contact-sec'>
                                <div className='contact-icon'>
                                        <FaEnvelope color='#63ab45'/>
                                    </div>
                                    <div className='contact-infos'>
                                        <p className='contact-info-header'> Email Address</p>
                                        <p className='contact-info-body'>contact@example.com</p>
                                    </div>
                                </div>
                            <div className='footer-contact-sec'>
                                <div className='contact-icon'>
                                        <FaLocationDot color='#63ab45'/>
                                    </div>
                                    <div className='contact-infos'>
                                        <p className='contact-info-header'>Visit office</p>
                                        <p className='contact-info-body'>583 Main Street, NY, USA</p>
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
