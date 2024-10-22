import { Autoplay, EffectFade } from "swiper/modules";
import { Swiper, SwiperSlide } from "swiper/react";

const PlacesTopSection: React.FC = () => {
    return (
      <div className="about-top">
        <Swiper
            effect={'fade'}
            centeredSlides={true}
            loop={true}
            autoplay={{
                delay: 2500,
                disableOnInteraction: false,
              }}
            modules={[EffectFade, Autoplay]}
            className="mySwiper"
            >
            <SwiperSlide
            style={{maxHeight: '300px' }}>
              <div className="slide-content">
                <img className="about-top-img" src="https://gaviaspreview.com/wp/gowilds/wp-content/uploads/2023/01/breadcrumb-01.jpg" />
                <div className="text-overlay">
                    <h2 className="about-top-h2">Explore The Worlds</h2>
                    <p className="about-top-p">People Don’t Take, Trips Take People</p>
                </div>
              </div>
            </SwiperSlide>
            <SwiperSlide
            style={{maxHeight: '300px' }}>
            <div className="slide-content">
                <img className="about-top-img" src="https://gaviaspreview.com/wp/gowilds/wp-content/uploads/2023/01/breadcrumb-02.jpg" />
                <div className="text-overlay">
                    <h2 className="about-top-h2">Explore The Worlds</h2>
                    <p className="about-top-p">People Don’t Take, Trips Take People</p>
                </div>
              </div>
            </SwiperSlide>
        </Swiper>
      </div>
    );
  }
  
  export default PlacesTopSection;