import '../styles/ErrorPageStyles.css'
import { PiArrowCircleLeftBold} from 'react-icons/pi';

const ErrorPage: React.FC = () => {
    return (
      <div className="error-content">
        <div className="error-img-sec">
          <img src="https://gaviaspreview.com/wp/gowilds/wp-content/themes/gowilds/assets/images/404-image.png" alt="" />
        </div>
        <h2>OPPS! This page is not found</h2>
        <p className='error-content-p'>The page requested could not be found. This could be a spelling error in the URL or a removed page.</p>
        <button className='back-homepage-btn'>
          <PiArrowCircleLeftBold/>
          <p className='back-homepage-btn-p'>Back Homepage</p>
        </button>
      </div>
    );
  }
  
  export default ErrorPage;