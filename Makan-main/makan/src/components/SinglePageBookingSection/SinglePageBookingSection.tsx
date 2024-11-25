import React, { useState } from "react";
import { DatePicker, Button, message } from "antd";
import { DollarCircleOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import PaymentModal from "../../components/PaymentModal/PaymentModal"; 
import "./SinglePageBookingSectionStyles.css";
import axios from "axios";

interface SinglePageBookingSectionProps {
  price: number;
  placeId: number;
  category: number;
}

const SinglePageBookingSection: React.FC<SinglePageBookingSectionProps> = ({
  price,
  placeId,
  category,
}) => {
  const [selectedDate, setSelectedDate] = useState<any>(null);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(false);
  const [isPaymentModalVisible, setPaymentModalVisible] = useState(false);
  const navigate= useNavigate();
  const totalPrice = (price * quantity).toFixed(2);

  const handleDateChange = (date: any) => {
    setSelectedDate(date);
  };

  const handleBooking = () => {
    if (!selectedDate) {
      message.error("Please select a date.");
      return;
    }

    if (category !== 2) {
      message.error("Booking is only available for entertainment places.");
      return;
    }

    setPaymentModalVisible(true); 
  };

  const handlePaymentSuccess = async () => {
    setLoading(true);
    setPaymentModalVisible(false);

    try {
      const userId = localStorage.getItem("id");
      const token = localStorage.getItem("token");
      const bookingResponse = await axios.post(
        `${import.meta.env.VITE_API_URL}/bookings`,
        {
          user_id: parseInt(userId!, 10),
          place_id: placeId,
          booking_date: selectedDate.format("YYYY-MM-DD"),
          status: "confirmed",
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (bookingResponse.status === 201) {
        const bookingId = bookingResponse.data.data.id;
        const totalCost = price * quantity; 
        try {
          const paymentResponse = await axios.post(
            `${import.meta.env.VITE_API_URL}/payments`,
            {
              booking_id: bookingId,
              amount: totalCost,
              transaction_date: new Date().toISOString().split("T")[0], 
              transaction_status: "completed",
            },
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
        } catch (error) {
          console.log(error)
            await axios.put(
              `${import.meta.env.VITE_API_URL}/bookings/${bookingId}`,
              { status: "cancelled" },
              {
                headers: { Authorization: `Bearer ${token}` },
              }
            );
            navigate("/bookings"); 
          
        }

        message.success("Booking confirmed!");
        
        navigate("/bookings");
      } else {
        message.error("Booking failed.");
      }
    } catch (error) {
      console.error("Error during booking:", error);
      message.error("An error occurred while confirming your booking.");
    } finally {
      setLoading(false);
    }
  };

  const incrementQuantity = () => {
    setQuantity((prev) => prev + 1);
  };

  const decrementQuantity = () => {
    setQuantity((prev) => (prev > 1 ? prev - 1 : 1));
  };

  return (
    <div className="booking-section">
      <h3>Book Your Ticket</h3>
      <DatePicker
        onChange={handleDateChange}
        placeholder="Select Date"
        style={{ width: "100%" }}
      />
      <div className="quantity-section">
        <Button onClick={decrementQuantity} className="quantity-button">
          -
        </Button>
        <span className="quantity-display">{quantity}</span>
        <Button onClick={incrementQuantity} className="quantity-button">
          +
        </Button>
      </div>
      <div className="price-section">
        <DollarCircleOutlined style={{ color: "#4CAF50", marginRight: "5px" }} />
        Total: ${totalPrice}
      </div>
      <Button
        type="primary"
        onClick={handleBooking}
        className="add-to-basket-button"
        disabled={loading}
      >
        {loading ? "Processing..." : "Book Now"}
      </Button>

      <PaymentModal
        isVisible={isPaymentModalVisible}
        amount={parseFloat(totalPrice)}
        onCancel={() => setPaymentModalVisible(false)}
        onPaymentSuccess={handlePaymentSuccess}
      />
    </div>
  );
};

export default SinglePageBookingSection;
