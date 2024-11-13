import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Card from '../Card/Card';
import './PlaceResultsSectionStyles.css';
import { Pagination, PaginationProps } from 'antd';

interface Place {
  id: number;
  name: string;
  location: string;
  rating: number;
  price: number;
}

interface PlaceResultsSectionProps {
  sortOption: string;
  isAscending: boolean;
}

const itemRender: PaginationProps['itemRender'] = (_, type, originalElement) => {
  if (type === 'prev') return <a>Previous</a>;
  if (type === 'next') return <a>Next</a>;
  return originalElement;
};

const PlaceResultsSection: React.FC<PlaceResultsSectionProps> = ({ sortOption, isAscending }) => {
  const [places, setPlaces] = useState<Place[]>([]);

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/places`); 
        setPlaces(response.data);
      } catch (error) {
        console.error('Error fetching places:', error);
      }
    };
    fetchPlaces();
  }, []);

  const sortedPlaces = [...places].sort((a, b) => {
    if (sortOption === 'price') {
      return isAscending ? a.price - b.price : b.price - a.price;
    } else if (sortOption === 'location') {
      return isAscending ? a.location.localeCompare(b.location) : b.location.localeCompare(a.location);
    } else if (sortOption === 'rating') {
      return isAscending ? a.rating - b.rating : b.rating - a.rating;
    }
    return 0;
  });

  return (
    <div>
      <div className="result-cards-sec">
        {sortedPlaces.map((place) => (
          <Card key={place.id} id={place.id} name={place.name} location={place.location} rating={place.rating} />
        ))}
      </div>
      <Pagination itemRender={itemRender} />
    </div>
  );
};

export default PlaceResultsSection;
