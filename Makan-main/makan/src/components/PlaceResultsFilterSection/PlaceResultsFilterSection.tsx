import { Select } from "antd";
import { FaSortAlphaDownAlt, FaSortAlphaUpAlt } from "react-icons/fa";
import './PlaceResultsFilterSectionStyles.css';

interface PlaceResultsFilterSectionProps {
  placesCount: number;
  sortOption: string;
  isAscending: boolean;
  onSortChange: (option: string, order: boolean) => void;
}

const PlaceResultsFilterSection: React.FC<PlaceResultsFilterSectionProps> = ({ placesCount, sortOption, isAscending, onSortChange }) => {
  const toggleSortOrder = (): void => {
    onSortChange(sortOption, !isAscending);
  };

  const handleOptionChange = (value: string) => {
    onSortChange(value, isAscending); 
  };

  return (
    <div className="place-result-filter-sec">
      <div className="place-result-filter-sec-left">
        <p className="gray-p filter-sec-p">
          <strong>{placesCount}</strong> Places
        </p>
      </div>
      <div className="place-result-filter-sec-right">
        <p className="gray-p filter-sec-p">Sort by</p>
        <div onClick={toggleSortOrder} style={{ cursor: 'pointer' }}>
          {isAscending ? <FaSortAlphaDownAlt color="gray" /> : <FaSortAlphaUpAlt color="gray" />}
        </div>
        <Select
          size="large"
          showSearch
          placeholder="Select"
          style={{ width: '100%' }}
          onChange={handleOptionChange}
          value={sortOption}
          options={[
            { value: 'price', label: 'Price' },
            { value: 'location', label: 'Location' },
            { value: 'rating', label: 'Rating' },
          ]}
        />
      </div>
    </div>
  );
};

export default PlaceResultsFilterSection;
