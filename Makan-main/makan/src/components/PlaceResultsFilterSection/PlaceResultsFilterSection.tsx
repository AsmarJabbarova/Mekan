import { Select } from "antd";
import { useState } from "react";
import { FaSortAlphaDownAlt, FaSortAlphaUpAlt, FaSortDown } from "react-icons/fa";
import './PlaceResultsFilterSectionStyles.css';


const PlaceResultsFilterSection: React.FC = () => {
  // State to control which icon is visible
const [isAscending, setIsAscending] = useState<boolean>(true);

// Function to toggle the state
const toggleSortOrder = (): void => {
  setIsAscending(!isAscending); // Toggle between true and false
};
    return (
      <div className="place-result-filter-sec">
        <div className="place-result-filter-sec-left">
          <p className="gray-p filter-sec-p">
            <strong> 12 </strong> 
             Places</p>
        </div>
        <div className="place-result-filter-sec-right">
          <p className="gray-p filter-sec-p">Sort by</p>
          <div onClick={toggleSortOrder} style={{ cursor: 'pointer' }}>
            {isAscending ? (
              <FaSortAlphaDownAlt color="gray" />
              ) : (
              <FaSortAlphaUpAlt color="gray" />
            )}
          </div>
          <Select
          size='large'
          showSearch
          placeholder="Select"
          style={{ width: '100%' }}
          filterOption={(input, option) =>
            (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
          }
          options={[
            { value: '1', label: 'Price' },
            { value: '2', label: 'Location' },
            { value: '3', label: 'Rating' },
          ]}
        />
        </div>
      </div>
    );
  }
  
  export default PlaceResultsFilterSection;