import React from 'react';
import Card from '../Card/Card';
import { Pagination } from 'antd';
import './PlaceResultsSectionStyles.css';

interface PlaceResultsSectionProps {
  places: any[];
  sortOption: string;
  isAscending: boolean;
}

const PlaceResultsSection: React.FC<PlaceResultsSectionProps> = ({ places }) => {
  const pageSize = 6;
  const [currentPage, setCurrentPage] = React.useState(1);

  const startIndex = (currentPage - 1) * pageSize;
  const paginatedPlaces = places.slice(startIndex, startIndex + pageSize);

  return (
    <div>
      <div className="result-cards-sec">
        {paginatedPlaces.map((place) => (
          <Card
            key={place.id}
            id={place.id}
            name={place.name}
            images={place.images}
            rating={place.rating}
            price={place.default_price} 
            location={place.location}          />
        ))}
      </div>
      <Pagination
        current={currentPage}
        pageSize={pageSize}
        total={places.length}
        onChange={(page) => setCurrentPage(page)}
        style={{ textAlign: 'center', marginTop: '20px' }}
      />
    </div>
  );
};

export default PlaceResultsSection;
