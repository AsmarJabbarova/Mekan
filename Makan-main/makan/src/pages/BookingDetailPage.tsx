import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Card, message, Spin } from "antd";
import axios from "axios";

interface BookingDetail {
  id: number;
  place_id: number;
  booking_date: string;
  status: string;
  total_cost: number;
  payment_status: string;
  place_name: string; 
}

const BookingDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [booking, setBooking] = useState<BookingDetail | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchBookingDetails = async () => {
      setLoading(true);
      const token = localStorage.getItem("token");

      if (!token) {
        message.error("User not logged in.");
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get(
          `${import.meta.env.VITE_API_URL}/bookings/${id}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setBooking(response.data.data);
      } catch (error) {
        console.error("Error fetching booking details:", error);
        message.error("Failed to load booking details.");
      } finally {
        setLoading(false);
      }
    };

    fetchBookingDetails();
  }, [id]);

  if (loading) return <Spin size="large" />;
  if (!booking) return <p>No booking details found.</p>;

  return (
    <Card title={`Booking Details - ID: ${booking.id}`}>
      <p><strong>Place Name:</strong> {booking.place_name}</p>
      <p><strong>Booking Date:</strong> {booking.booking_date}</p>
      <p><strong>Status:</strong> {booking.status}</p>
      <p><strong>Total Cost:</strong> ${booking.total_cost}</p>
      <p><strong>Payment Status:</strong> {booking.payment_status}</p>
    </Card>
  );
};

export default BookingDetailPage;
