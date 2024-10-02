import { FaArrowRight } from 'react-icons/fa';
import './AdventureCardStyles.css'

const AdventureCard: React.FC = () => {

    return (
      <div className="inner-card-image">
        <div className="banner-inner">
          <div className='banner-inner-top'>
            <div className="banner-inner-top">Adventure and climbing</div>
            <div className='arrow-sec-card green-card'>
              <FaArrowRight className='arrow-icon-card'/>
            </div>
          </div>
            <div className="banner-inner-desc">Lorem ipsum, dolor sit amet consectetur adipisicing elit. </div>
        </div>
      </div>
    );
  }
  
  export default AdventureCard;
  