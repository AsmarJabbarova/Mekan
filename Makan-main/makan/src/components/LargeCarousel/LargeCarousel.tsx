import React from 'react';
import { Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import './LargeCarouselStyles.css';

interface Place {
  id: number;
  name: string;
  description: string;
  images: string[];
}

interface LargeCarouselProps {
  places: Place[];
}

const LargeCarousel: React.FC<LargeCarouselProps> = ({ places }) => {
  return (
    <div id="carouselExampleCaptions" className="carousel slide carousel-fade" data-bs-ride="carousel">
      <div className="carousel-inner">
        {places.map((place, index) => (
          <div key={place.id} className={`carousel-item ${index === 0 ? 'active' : ''}`}>
            <Link to={`/place/${place.id}`}>
              <img
                src={place.images[0]}
                className="d-block w-100 custom-slider-image"
                alt={place.name}
              />
            </Link>
            <div className="custom-carousel-caption">
              <h5 className="custom-carousel-title">{place.name}</h5>
              <p className="custom-carousel-description">{place.description}</p>
            </div>
          </div>
        ))}
      </div>
      <button
        className="carousel-control-prev"
        type="button"
        data-bs-target="#carouselExampleCaptions"
        data-bs-slide="prev"
      >
        <span className="carousel-control-prev-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Previous</span>
      </button>
      <button
        className="carousel-control-next"
        type="button"
        data-bs-target="#carouselExampleCaptions"
        data-bs-slide="next"
      >
        <span className="carousel-control-next-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Next</span>
      </button>
    </div>
  );
};

export default LargeCarousel;
