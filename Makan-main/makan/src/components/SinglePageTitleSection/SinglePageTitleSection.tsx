import { FaLocationDot } from 'react-icons/fa6';
import './SinglePageTitleSectionStyles.css'

const SinglePageTitleSection: React.FC = () => {
    return (
      <div className="single-title-sec">
        <div className="single-title-sec-left">
            <h2>Beautiful Floating Villa</h2>
            <div className="single-title-sec-left-inner">
                <FaLocationDot color='#63ab45'/>
                <p className='gray-p'>Main Street, Brooklyn, NY</p>
            </div>
        </div>
        <div className="single-title-sec-right">
            <h4 className='gray-p'>Category</h4>
            <p>Adventure</p>
        </div>
      </div>
    );
  }
  
  export default SinglePageTitleSection;