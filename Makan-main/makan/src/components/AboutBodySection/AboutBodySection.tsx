import './AboutBodySectionStyles.css'
const AboutBodySection: React.FC = () => {
    return (
      <div className='about-body'>
        <div className='about-sec-inner-div'>
                <div className='about-inner-left-sec'>
                    <div className='about-inner-left-lg-img-sec'>
                        <img className='about-inner-left-lg-img' src="https://gaviaspreview.com/wp/gowilds/wp-content/uploads/2023/02/image-20.jpg" alt="28"/>
                    </div>
                    <div className='about-inner-left-sm-img-sec'>
                        <img className='about-inner-left-sm-img' src="https://gaviaspreview.com/wp/gowilds/wp-content/uploads/2023/02/image-21.jpg" alt="28"/>
                    </div>
                </div>
                <div className='about-inner-right-sec'>
                    <div className="about-top-sec">
                        <div className="about-top-inner">
                            About Company
                        </div>
                    </div>
                    <div className="about-desc-sec">
                        Great opportunity for adventure & travels
                    </div>
                    <div className='features-list'>
                        <div className='feature-list-item'>
                            <div className='check-icon'></div>
                            <div className='feature-list-content'>
                                <div className='feature-list-content-title'>Safety first always</div>
                                <div className='feature-list-content-desc'>Set perspiciatis unde omnis estenatus voluptatem totarem aperiae.</div>
                            </div>
                        </div>
                        <div className='feature-list-item'>
                            <div className='check-icon'></div>
                            <div className='feature-list-content'>
                                <div className='feature-list-content-title'> Low price & friendly</div>
                                <div className='feature-list-content-desc'>Quis autem vel eum iure voluptate velit esse nihile consequatur.</div>
                            </div>
                        </div>
                        <div className='feature-list-item'>
                            <div className='check-icon'></div>
                            <div className='feature-list-content'>
                                <div className='feature-list-content-title'>Trusted travel guide</div>
                                <div className='feature-list-content-desc'>At vero accusamus dignissimos ducimus blanditiis deleniti atque quos.</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
      </div>
    );
  }
  
  export default AboutBodySection;