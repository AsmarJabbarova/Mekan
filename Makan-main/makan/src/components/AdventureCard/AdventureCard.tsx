import { FaArrowRight } from 'react-icons/fa';
import './AdventureCardStyles.css';
import { Link } from 'react-router-dom';

interface AdventureCardProps {
  place: {
    id: number;
    name: string;
    location: string;
    rating: number;
    description: string;
  };
}

const AdventureCard: React.FC<AdventureCardProps> = ({ place }) => {
  return (
    <Link to={`/place/${place.id}`} className="inner-card-image">
      <div className="banner-inner">
        <div className='banner-inner-top'>
          <div className="banner-inner-title">{place.name}</div>
          <div className='arrow-sec-card green-card'>
            <FaArrowRight className='arrow-icon-card'/>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default AdventureCard;
