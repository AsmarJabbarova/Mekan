import { Pagination, PaginationProps } from 'antd';
import Card from '../Card/Card';
import './PlaceResultsSectionStyles.css'

const itemRender: PaginationProps['itemRender'] = (_, type, originalElement) => {
  if (type === 'prev') {
    return <a>Previous</a>;
  }
  if (type === 'next') {
    return <a>Next</a>;
  }
  return originalElement;
};


const PlaceResultsSection: React.FC = () => {
    return (
      <div >
        <div className="result-cards-sec">
          <Card/>
          <Card/>
          <Card/>
          <Card/>
          <Card/>
          <Card/>
        </div>
        <Pagination
          itemRender={itemRender} />
      </div>
      
    );
  }
  
  export default PlaceResultsSection;