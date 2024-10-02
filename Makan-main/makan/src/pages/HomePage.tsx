import '../styles/HomepageStyles.css'
import AdventureCard from "../components/AdventureCard/AdventureCard";
import LargeCarousel from "../components/LargeCarousel/LargeCarousel";
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Scrollbar, A11y } from 'swiper/modules';

import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css/scrollbar';
import HomeAboutSection from '../components/HomeAboutSection/HomeAboutSection';

const HomePage: React.FC = () => {

    return (
      <div>
        <div className="home-top-sec">
          <LargeCarousel/>
        </div>
        <div className="popular-activities-sec">
          <div className="popular-activites-top-sec">
            <div className="popular-activites-top-inner">
              Popular Activities
            </div>
          </div>
          <div className="popular-activites-desc-sec">
            Explore Real Adventure
          </div>
          <Swiper
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
            loop={true}
            navigation
            pagination={{ clickable: true }}
            onSwiper={(swiper) => console.log(swiper)}
            onSlideChange={() => console.log('slide change')}>
            <SwiperSlide>
              <AdventureCard/>
            </SwiperSlide>
            <SwiperSlide>
              <AdventureCard/>
            </SwiperSlide>
            <SwiperSlide>
              <AdventureCard/>
            </SwiperSlide>
            <SwiperSlide>
              <AdventureCard/>
            </SwiperSlide>
            <SwiperSlide>
              <AdventureCard/>
            </SwiperSlide>
            <SwiperSlide>
              <AdventureCard/>
            </SwiperSlide>
          </Swiper>
        </div>
        <HomeAboutSection/>
      </div>
    );
  }
  
  export default HomePage;
  