import { useState, useEffect } from 'react';
import { Select, Slider, Radio } from 'antd';
import { StarFilled, StarOutlined } from '@ant-design/icons';
import { FaSearch } from 'react-icons/fa';
import './PlacesFilterSection.css';
import axios from 'axios';
import { Place } from '../../models/Place';

interface Category {
  id: number;
  name: string;
}

interface EntertainmentType {
  id: number;
  name: string;
}

interface PlacesFilterSectionProps {
  onFilterChange: (filters: {
    category: string | null;
    adventureType: string | null;
    city: string | null;
    priceRange: [number, number];
    rating: number | null;
  }) => void;
}

const PlacesFilterSection: React.FC<PlacesFilterSectionProps> = ({ onFilterChange }) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [cities, setCities] = useState<string[]>([]);
  const [entertainmentTypes, setEntertainmentTypes] = useState<EntertainmentType[]>([]);
  const [category, setCategory] = useState<string | null>(null);
  const [adventureType, setAdventureType] = useState<string | null>(null);
  const [priceRange, setPriceRange] = useState<[number, number]>([0, 1000]);
  const [rating, setRating] = useState<number | null>(null);
  const [city, setCity] = useState<string | null>(null);


  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const categoriesResponse = await axios.get<{ data: Category[] }>(
          `${import.meta.env.VITE_API_URL}/place_categories`
        );
        setCategories(categoriesResponse.data.data);

        const entertainmentTypesResponse = await axios.get<{ data: EntertainmentType[] }>(
          `${import.meta.env.VITE_API_URL}/entertainment_types`
        );
        setEntertainmentTypes(entertainmentTypesResponse.data.data);

        const placesResponse = await axios.get<{ data: Place[] }>(
          `${import.meta.env.VITE_API_URL}/places`
        );
        const allPlaces = placesResponse.data.data;
        const uniqueCities = Array.from(new Set(allPlaces.map((place) => place.city)));
        setCities(uniqueCities);
      } catch (error) {
        console.error('Error fetching filter options:', error);
      }
    };

    fetchOptions();
  }, []);

  const handleSearch = () => {
    const filters = {
      category,
      adventureType,
      city,
      priceRange,
      rating,
    };
    onFilterChange(filters);
  };

  return (
    <div className="side-filter-sec">

      <Select
        size="large"
        showSearch
        placeholder="Place Category"
        style={{ width: '100%' }}
        onChange={(value) => setCategory(value)}
        options={categories.map((cat) => ({ value: cat.id.toString(), label: cat.name }))}
      />
      <Select
        size="large"
        showSearch
        placeholder="Entertainment Type"
        style={{ width: '100%' }}
        onChange={(value) => setAdventureType(value)}
        options={entertainmentTypes.map((type) => ({ value: type.id.toString(), label: type.name }))}
      />
      <Select
        size="large"
        showSearch
        placeholder="City"
        style={{ width: '100%' }}
        onChange={(value) => setCity(value)}
        options={cities.map((city) => ({ value: city, label: city }))}
      />
      <div className="slider-container">
        <p className='gray-p filter-label'>Price</p>
        <Slider
          style={{ 
            width: '95%', }}
          range
          className="custom-slider"
          defaultValue={[0, 500]}
          max={500}
          onChange={(value) => setPriceRange(value as [number, number])}
        />
        <div className="slider-labels ">
          <span className="slider-min">0</span>
          <span className="slider-max">500</span>
        </div>
      </div>
      <div>
        <p className='gray-p filter-label'>Rating</p>
        <Radio.Group
          className="filter-rate-sec"
          onChange={(e) => setRating(e.target.value)}
        >
          {[5, 4, 3, 2, 1].map((stars) => (
            <Radio key={stars} value={stars}>
              {[...Array(stars)].map((_, i) => (
                <StarFilled key={i} style={{ color: '#F7931E' }} />
              ))}
              {[...Array(5 - stars)].map((_, i) => (
                <StarOutlined key={i} style={{ color: '#F7931E' }} />
              ))}
            </Radio>
          ))}
        </Radio.Group>
      </div>
      <button type="button" className="submit-button" onClick={handleSearch}>
        <FaSearch /> Search
      </button>
    </div>
  );
};

export default PlacesFilterSection;
