import { FaLocationDot } from 'react-icons/fa6';
import './SinglePageTitleSectionStyles.css'

interface SinglePageTitleSectionProps {
  title?: string;
  location?: string;
  entertainment_type?: string;
}

const SinglePageTitleSection: React.FC<SinglePageTitleSectionProps> = ({ title, location, entertainment_type}) => {
  return (
      <div className="single-title-sec">
        <div className="single-title-sec-left">
            <h2>{title || "Default Title"}</h2>
            <div className="single-title-sec-left-inner">
                <FaLocationDot color='#63ab45'/>
                <p className='gray-p'>{location || "Location not available"}</p>
            </div>
        </div>
        <div className="single-title-sec-right">
            <h4 className='gray-p'>Category</h4>
            <p>{entertainment_type || "Entertainment not available"}</p>
        </div>
      </div>
    );
  }
  
  export default SinglePageTitleSection;