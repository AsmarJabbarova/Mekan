import React, { useState } from 'react';
import { DatePicker, Button, message } from 'antd';
import { DollarCircleOutlined } from '@ant-design/icons';
import './SinglePageBookingSectionStyles.css';

const TICKET_PRICE = 15.0; // Price per ticket

const SinglePageBookingSection: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState(null);
  const [quantity, setQuantity] = useState(1);

  const handleDateChange = (date: any) => {
    setSelectedDate(date);
  };

  const handleAddToBasket = () => {
    if (!selectedDate) {
      message.error('Please select a date.');
      return;
    }
    message.success(`Added ${quantity} ticket(s) for ${selectedDate.format('YYYY-MM-DD')} to basket!`);
  };

  const incrementQuantity = () => {
    setQuantity((prev) => prev + 1);
  };

  const decrementQuantity = () => {
    setQuantity((prev) => (prev > 1 ? prev - 1 : 1));
  };

  const totalPrice = (quantity * TICKET_PRICE).toFixed(2);

  return (
    <div className="booking-section">
      <h3>Book Your Ticket</h3>
      <DatePicker 
        onChange={handleDateChange}
        placeholder="Select Date"
        style={{ width: '100%' }}
      />
      <div className="quantity-section">
        <Button onClick={decrementQuantity} className="quantity-button">-</Button>
        <span className="quantity-display">{quantity}</span>
        <Button onClick={incrementQuantity} className="quantity-button">+</Button>
      </div>
      <div className="price-section">
        <DollarCircleOutlined style={{ color: '#4CAF50', marginRight: '5px' }} />
        Total: ${totalPrice}
      </div>
      <Button 
        type="primary"
        onClick={handleAddToBasket}
        className="add-to-basket-button"
      >
        Add to Basket
      </Button>
    </div>
  );
};

export default SinglePageBookingSection;
