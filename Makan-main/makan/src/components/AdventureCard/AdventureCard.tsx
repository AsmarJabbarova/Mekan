import { FaArrowRight } from 'react-icons/fa';
import './AdventureCardStyles.css';
import { Link } from 'react-router-dom';

interface AdventureCardProps {
  place: {
    id: number;
    name: string;
    description: string;
    images: string[];
  };
}

const AdventureCard: React.FC<AdventureCardProps> = ({ place }) => {
  return (
    <Link to={`/place/${place.id}`} className="inner-card-image" 
    style={{ backgroundImage: `url(${place.images?.[0] || 'https://gaviaspreview.com/wp/gowilds/wp-content/uploads/2022/12/image-03.jpg'})` }}>
      <div className="banner-inner">
        <div className='banner-inner-top'>
          <div className="banner-inner-title">{place.name}</div>
          <div className='arrow-sec-card green-card'>
            <FaArrowRight className='arrow-icon-card'/>
          </div>
        </div>
        <div className="banner-inner-desc">{place.description}</div>
      </div>
    </Link>
  );
};

export default AdventureCard;
