import React from 'react';
import { Navigate } from 'react-router-dom';
import { useUser } from '../contexts/UserContext';

const AdminRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const { role } = useUser();
  
    if (role === null) {
      return <div>Loading...</div>;
    }
  
    if (role !== 'admin') {
      return <Navigate to="/unauthorized" />;
    }
  
    return <>{children}</>;
  };
  
  export default AdminRoute;
  
