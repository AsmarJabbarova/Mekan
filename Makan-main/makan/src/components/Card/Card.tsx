import React from 'react';
import { Link } from 'react-router-dom';
import { Rate } from 'antd';
import { HeartFilled } from '@ant-design/icons';
import { FaCircleDollarToSlot, FaLocationDot } from 'react-icons/fa6';
import './CardStyles.css';

interface CardProps {
  id: number;
  name: string;
  location: string;
  rating: number;
  images: string[];
  price: number;
}

const Card: React.FC<CardProps> = ({ id, name, location, rating, images, price }) => {
  return (
    <div className='card'>
      <div className='img-sec'>
        <Link to={`/place/${id}`} className='card-link'>
            <img className='place-image' src={images?.[0]} alt="" />
        </Link>
      </div>
      <div className='card-info-sec'>
        <div className='card-info-top-sec'>
          <Rate allowHalf disabled defaultValue={rating} style={{ color: '#F7931E', fontSize: 15 }} />
          <div className='card-fav-sec'>
            <Rate character={<HeartFilled />} count={1} style={{ color: '#D22B2B', fontSize: 15 }} />
          </div>
        </div>
        <Link to={`/place/${id}`} className='card-link'>
          <div className='card-place-name-sec'>{name}</div>
        </Link>
        <div className='card-desc-sec'>
          <FaLocationDot color='#63ab45' />
          <p className='card-address gray-p'>{location}</p>
        </div>
        <div className='card-desc-sec'>
          <FaCircleDollarToSlot color='#63ab45' />
          <p className='orange-p'>${price}</p>
        </div>
      </div>
    </div>
  );
};

export default Card;
