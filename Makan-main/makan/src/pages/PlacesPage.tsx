import PlaceResultsFilterSection from "../components/PlaceResultsFilterSection/PlaceResultsFilterSection";
import PlaceResultsSection from "../components/PlaceResultsSection/PlaceResultsSection";
import PlacesFilterSection from "../components/PlacesFilterSection/PlacesFilterSection";
import PlacesTopSection from "../components/PlacesTopSection/PlacesTopSection";
import '../styles/PlacesPageStyles.css'

const PlacesPage: React.FC = () => {
    return (
      <div className="places-main">
        <PlacesTopSection/>
        <div  className="place-results-sec">
          <div className="place-results-sec-inner">
            <PlacesFilterSection/>
          <div className="place-results-sec-right">
            <PlaceResultsFilterSection/>
            <PlaceResultsSection/>
          </div>
        </div>
        </div>
      </div>
    );
  }
  
  export default PlacesPage;