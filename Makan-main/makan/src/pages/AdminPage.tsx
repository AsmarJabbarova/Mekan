import React, { useState } from 'react';
import '../styles/AdminPageStyles.css';
import CRUDOperations from '../components/CRUDPanel/CRUDPanel';

const models = [
  'Company',
  'Language',
  'EntertainmentType',
  'PlaceCategory',
  'User',
  'UserPreference',
  'UserAudit',
  'UserSession',
  'Place',
  'PricingRule',
  'Promotion',
  'Driver',
  'Assignment',
  'Booking',
  'BookingTransaction',
  'Payment',
  'Currency',
  'Availability',
  'Review',
  'ReviewMedia',
  'Transportation',
  'PlaceTranslation',
  'EmergencyContact',
  'RouteSegment',
];

const AdminPage: React.FC = () => {
  const [selectedModel, setSelectedModel] = useState<string | null>(null);

  const handleModelSelect = (model: string) => {
    setSelectedModel(model);
  };

  return (
    <div className="admin-page">
      <h1 >Admin Dashboard</h1>
      <div className="model-buttons">
        {models.map((model) => (
          <button
            key={model}
            className="model-button"
            onClick={() => handleModelSelect(model)}
          >
            {model}
          </button>
        ))}
      </div>

      {selectedModel ? (
        <div className="crud-panel">
          <h2>{selectedModel} Admin Panel</h2>
          <CRUDOperations modelName={selectedModel} />
        </div>
      ) : (
        <p className="no-selection">Please select a model to manage.</p>
      )}
    </div>
  );
};

export default AdminPage;
