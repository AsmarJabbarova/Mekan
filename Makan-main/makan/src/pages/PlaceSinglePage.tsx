import SinglePageBookingSection from "../components/SinglePageBookingSection/SinglePageBookingSection";
import SinglePageDescriptionSection from "../components/SinglePageDescriptionSection/SinglePageDescriptionSection";
import SinglePageReviewSection from "../components/SinglePageReviewSection/SinglePageReviewSection";
import SinglePageTitleSection from "../components/SinglePageTitleSection/SinglePageTitleSection";
import SinglePageTopSection from "../components/SinglePageTopSection/SinglePageTopSection";

import '../styles/PlaceSinglePageStyles.css'

const PlaceSinglePage: React.FC = () => {
    return (
      <div>
        <SinglePageTopSection/>
        <SinglePageTitleSection/>
        <div className="single-page-body">
          <div className="single-page-body-inner">
          <div>
            <SinglePageDescriptionSection/>
            <SinglePageReviewSection/>
          </div>
          <SinglePageBookingSection/>
          </div>
        </div>
      </div>
    );
  }
  
  export default PlaceSinglePage;