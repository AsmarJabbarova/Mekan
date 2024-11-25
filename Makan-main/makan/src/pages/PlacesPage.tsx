import { useState, useEffect } from 'react';
import axios from 'axios';
import PlaceResultsFilterSection from '../components/PlaceResultsFilterSection/PlaceResultsFilterSection';
import PlaceResultsSection from '../components/PlaceResultsSection/PlaceResultsSection';
import PlacesFilterSection from '../components/PlacesFilterSection/PlacesFilterSection';
import PlacesTopSection from '../components/PlacesTopSection/PlacesTopSection';
import '../styles/PlacesPageStyles.css';

const PlacesPage: React.FC = () => {
  const [places, setPlaces] = useState([]);  
  const [filteredPlaces, setFilteredPlaces] = useState([]);
  const [sortOption, setSortOption] = useState<string>('rating');
  const [isAscending, setIsAscending] = useState<boolean>(false);

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/places`);
        setPlaces(response.data.data);
        setFilteredPlaces(response.data.data); 
      } catch (error) {
        console.error('Error fetching places:', error);
      }
    };
    fetchPlaces();
  }, []);


  // sorting
  const handleSortChange = (option: string, order: boolean) => {
    setSortOption(option);
    setIsAscending(order);
    const sorted = [...filteredPlaces].sort((a, b) => {
      if (option === 'price') {
        return order ? a.default_price - b.default_price : b.default_price - a.default_price;
      } else if (option === 'rating') {
        return order ? a.rating - b.rating : b.rating - a.rating;
      } else if (option === 'location') {
        return order
          ? a.location.localeCompare(b.location)
          : b.location.localeCompare(a.location);
      }
      return 0;
    });
    setFilteredPlaces(sorted);
  };



  //filters filter sectiondan qebul edilir
  const handleFilterChange = (filters: any) => {
    const filtered = places.filter((place) => {
      const matchCategory =
        !filters.category || place.category_id === parseInt(filters.category);

      const matchEntertainmentType =
        !filters.adventureType || place.entertainment_type_id === parseInt(filters.adventureType);

      const matchPrice =
        place.default_price >= filters.priceRange[0] &&
        place.default_price <= filters.priceRange[1];

      const matchRating = !filters.rating || place.rating >= filters.rating;

      const matchCity = !filters.city || place.city == filters.city;


      return matchCategory && matchEntertainmentType && matchPrice && matchRating && matchCity;
    });
    setFilteredPlaces(filtered);
  };

  return (
    <div className="places-main">
      <PlacesTopSection />
      <div className="place-results-sec">
        <div className="place-results-sec-inner">
          <PlacesFilterSection onFilterChange={handleFilterChange} />
          <div className="place-results-sec-right">
            <PlaceResultsFilterSection
              placesCount={filteredPlaces.length}
              sortOption={sortOption}
              isAscending={isAscending}
              onSortChange={handleSortChange}
            />
            <PlaceResultsSection
              places={filteredPlaces}
              sortOption={sortOption}
              isAscending={isAscending}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlacesPage;
