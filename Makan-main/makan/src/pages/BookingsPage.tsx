import React, { useEffect, useState } from "react";
import { Table, message, Spin } from "antd";
import axios from "axios";
import { useNavigate } from "react-router-dom";

interface Booking {
  id: number;
  user_id: number;
  place_id: number;
  booking_date: string;
  status: string;
  total_cost: number;
}

const BookingsPage: React.FC = () => {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchBookings = async () => {
      setLoading(true);
      const userId = localStorage.getItem("id");
      const token = localStorage.getItem("token");

      if (!userId || !token) {
        message.error("User not logged in.");
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/bookings`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        const allBookings = response.data.data;
        const userBookings = allBookings.filter((booking: Booking) => booking.user_id === Number(userId));
        setBookings(userBookings);
      } catch (error) {
        console.error("Error fetching bookings:", error);
        message.error("Failed to load bookings.");
      } finally {
        setLoading(false);
      }
    };

    fetchBookings();
  }, []);

  const columns = [
    { title: "Booking ID", dataIndex: "id", key: "id" },
    { title: "Place ID", dataIndex: "place_id", key: "place_id" },
    { title: "Booking Date", dataIndex: "booking_date", key: "booking_date" },
    { title: "Status", dataIndex: "status", key: "status" },
    { title: "Total Cost", dataIndex: "total_cost", key: "total_cost", render: (cost: number) => `$${cost}` },
    {
      title: "Action",
      key: "action",
      render: (_: any, record: Booking) => (
        <a onClick={() => navigate(`/booking/${record.id}`)}>View Details</a>
      ),
    },
  ];

  if (loading) return <Spin size="large" />;

  return (
    <div>
      <h2>Your Bookings</h2>
      <Table dataSource={bookings} columns={columns} rowKey="id" />
    </div>
  );
};

export default BookingsPage;
