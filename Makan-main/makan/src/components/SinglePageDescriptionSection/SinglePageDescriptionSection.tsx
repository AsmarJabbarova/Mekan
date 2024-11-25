import React from "react";
import "./SinglePageDescriptionSectionStyles.css";
import { Place } from "../../models/Place";

interface SinglePageDescriptionSectionProps {
  place: Place | null;
}

const SinglePageDescriptionSection: React.FC<SinglePageDescriptionSectionProps> = ({ place }) => {
  return (
    <div className="single-desc-sec">
      <div
        className="location-image"
        style={{
          backgroundImage: `url(${place.images[0] || 'default-image-url.jpg'})`,
          backgroundSize: "cover",
          height: "300px",
          borderRadius: "8px",
        }}
      ></div>
      <div className="gray-p">
        {place.description || "No description available for this place."}
      </div>
    </div>
  );
};

export default SinglePageDescriptionSection;
