import PlaceResultsFilterSection from "../components/PlaceResultsFilterSection/PlaceResultsFilterSection";
import PlaceResultsSection from "../components/PlaceResultsSection/PlaceResultsSection";
import PlacesFilterSection from "../components/PlacesFilterSection/PlacesFilterSection";
import PlacesTopSection from "../components/PlacesTopSection/PlacesTopSection";
import '../styles/PlacesPageStyles.css';
import { useState, useEffect } from 'react';
import axios from 'axios';

const PlacesPage: React.FC = () => {
  const [places, setPlaces] = useState([]);  
  const [sortOption, setSortOption] = useState<string>('rating');
  const [isAscending, setIsAscending] = useState<boolean>(false);

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

  const handleSortChange = (option: string, order: boolean) => {
    setSortOption(option);
    setIsAscending(order);
  };

  return (
    <div className="places-main">
      <PlacesTopSection/>
      <div className="place-results-sec">
        <div className="place-results-sec-inner">
          <PlacesFilterSection/>
          <div className="place-results-sec-right">
            <PlaceResultsFilterSection
              placesCount={places.length}
              sortOption={sortOption}
              isAscending={isAscending}
              onSortChange={handleSortChange}
            />
            <PlaceResultsSection sortOption={sortOption} isAscending={isAscending} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlacesPage;
