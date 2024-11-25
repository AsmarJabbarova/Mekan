import React, { useEffect, useState } from 'react';
import AdventureCard from "../components/AdventureCard/AdventureCard";
import LargeCarousel from "../components/LargeCarousel/LargeCarousel";
import HomeAboutSection from '../components/HomeAboutSection/HomeAboutSection';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Scrollbar, A11y } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css/scrollbar';
import axios from 'axios';
import '../styles/HomepageStyles.css';

interface Place {
  id: number;
  name: string;
  location: string;
  latitude?: number;
  longitude?: number;
  rating: number;
  description: string;
  entertainment_type_id: number;
  category_id?: number; 
  default_price?: number;
  images: string[];
}


const HomePage: React.FC = () => {
  const [places, setPlaces] = useState<Place[]>([]);

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/places`);
    console.log('Places:', response.data);
        setPlaces(response.data.data);
      } catch (error) {
        console.error('Error fetching places:', error);
      }
    };
    fetchPlaces();
  }, []);

  const latestPlaces = places.slice(0, 5);

  return (
    <div>
      <div className="home-top-sec">
      <LargeCarousel places={latestPlaces} />
      </div>
      <div className="popular-activities-sec">
        <div className="popular-activites-top-sec">
          <div className="popular-activites-top-inner">
            Popular Activities
          </div>
        </div>
        <div className="popular-activites-desc-sec" style={{ width : '100%'}}>
          Explore Real Adventure
        </div>
        <Swiper
         loop={true}
          style={{ borderRadius: '13px' }}
          modules={[Navigation, Scrollbar, A11y]}
          spaceBetween={35}
          slidesPerView={4}
          breakpoints={{
            300: {
              slidesPerView: 1,
            },
            640: {
              slidesPerView: 2,
              spaceBetween: 20,
            },
            1000: {
              slidesPerView: 3,
              spaceBetween: 30,
            },
            1400: {
              slidesPerView: 4,
              spaceBetween: 35,
            },
          }}
          navigation
          pagination={{ clickable: true }}
        >
          {places.map((place) => (
            <SwiperSlide key={place.id}>
              <AdventureCard place={place} />
            </SwiperSlide>
          ))}
        </Swiper>
      </div>
      <HomeAboutSection />
    </div>
  );
};

export default HomePage;
