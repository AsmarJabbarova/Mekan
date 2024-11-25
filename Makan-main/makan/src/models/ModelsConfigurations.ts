
export const modelConfigurations = {
    User: {
      fields: [
        { name: 'username', label: 'Username', type: 'text', required: true },
        { name: 'email', label: 'Email', type: 'email', required: true },
        { name: 'password', label: 'Password', type: 'password', required: true },
      ],
      endpoint: 'users',
    },
    Booking: {
      fields: [
        { name: 'user_id', label: 'User ID', type: 'number', required: true },
        { name: 'place_id', label: 'Place ID', type: 'number', required: true },
        { name: 'booking_date', label: 'Booking Date', type: 'date', required: true },
        { name: 'status', label: 'Status', type: 'text', required: true },
      ],
      endpoint: 'bookings',
    },
    Place: {
      fields: [
        { name: 'name', label: 'Name', type: 'text', required: true },
        { name: 'description', label: 'Description', type: 'text', required: true },
        { name: 'city', label: 'City', type: 'text', required: true },
        { name: 'location', label: 'Location', type: 'text', required: true },
        { name: 'latitude', label: 'Latitude', type: 'number', required: false },
        { name: 'longitude', label: 'Longitude', type: 'number', required: false },
        { name: 'rating', label: 'Rating', type: 'number', required: true },
        { name: 'entertainment_type_id', label: 'Entertainment Type ID', type: 'number', required: true },
        { name: 'category_id', label: 'Category ID', type: 'number', required: false },
        { name: 'default_price', label: 'Default Price', type: 'number', required: false },
        { name: 'images', label: 'Images', type: 'text', required: false },
      ],
      endpoint: 'places',
    },
    UserSession: {
      fields: [
        { name: 'user_id', label: 'User ID', type: 'number', required: true },
        { name: 'login_time', label: 'Login Time', type: 'datetime-local', required: true },
        { name: 'logout_time', label: 'Logout Time', type: 'datetime-local', required: true },
      ],
      endpoint: 'user_sessions',
    },
    Review: {
      fields: [
        { name: 'place_id', label: 'Place ID', type: 'number', required: true },
        { name: 'user_id', label: 'User ID', type: 'number', required: true },
        { name: 'rating', label: 'Rating', type: 'number', required: true },
        { name: 'comment', label: 'Comment', type: 'text', required: true },
      ],
      endpoint: 'reviews',
    },
    ReviewMedia: {
      fields: [
        { name: 'review_id', label: 'Review ID', type: 'number', required: true },
        { name: 'media_type', label: 'Media Type', type: 'text', required: true },
        { name: 'media_url', label: 'Media URL', type: 'text', required: true },
      ],
      endpoint: 'review_medias',
    },
    Promotion: {
      fields: [
        { name: 'code', label: 'Code', type: 'text', required: true },
        { name: 'discount', label: 'Discount', type: 'number', required: true },
        { name: 'valid_from', label: 'Valid From', type: 'date', required: true },
        { name: 'valid_to', label: 'Valid To', type: 'date', required: true },
      ],
      endpoint: 'promotions',
    },
    PricingRule: {
      fields: [
        { name: 'place_id', label: 'Place ID', type: 'number', required: true },
        { name: 'currency_id', label: 'Currency ID', type: 'number', required: true },
        { name: 'price', label: 'Price', type: 'number', required: true },
        { name: 'start_date', label: 'Start Date', type: 'date', required: true },
        { name: 'end_date', label: 'End Date', type: 'date', required: true },
      ],
      endpoint: 'pricing_rules',
    },
    PlaceTranslation: {
      fields: [
        { name: 'place_id', label: 'Place ID', type: 'number', required: true },
        { name: 'language_id', label: 'Language ID', type: 'number', required: true },
        { name: 'title', label: 'Title', type: 'text', required: true },
        { name: 'description', label: 'Description', type: 'text', required: true },
      ],
      endpoint: 'place_translations',
    },
    Language: {
      fields: [
        { name: 'name', label: 'Name', type: 'text', required: true },
      ],
      endpoint: 'languages',
    },
    Driver: {
      fields: [
        { name: 'company_id', label: 'Company ID', type: 'number', required: true },
        { name: 'name', label: 'Name', type: 'text', required: true },
        { name: 'surname', label: 'Surname', type: 'text', required: true },
        { name: 'age', label: 'Age', type: 'number', required: true },
        { name: 'language_id', label: 'Language ID', type: 'number', required: true },
        { name: 'status', label: 'Status', type: 'text', required: true },
      ],
      endpoint: 'drivers',
    },
    Currency: {
      fields: [
        { name: 'name', label: 'Name', type: 'text', required: true },
        { name: 'symbol', label: 'Symbol', type: 'text', required: true },
      ],
      endpoint: 'currencies',
    },
    EmergencyContact: {
      fields: [
        { name: 'user_id', label: 'User ID', type: 'number', required: true },
        { name: 'name', label: 'Name', type: 'text', required: true },
        { name: 'phone', label: 'Phone', type: 'text', required: true },
        { name: 'relation', label: 'Relation', type: 'text', required: true },
      ],
      endpoint: 'emergency_contacts',
    },
    EntertainmentType: {
      fields: [
        { name: 'name', label: 'Name', type: 'text', required: true },
      ],
      endpoint: 'entertainment_types',
    },
    Company: {
      fields: [
        { name: 'name', label: 'Name', type: 'text', required: true },
      ],
      endpoint: 'companies',
    },
    Assignment: {
      fields: [
        { name: 'driver_id', label: 'Driver ID', type: 'number', required: true },
        { name: 'place_id', label: 'Place ID', type: 'number', required: true },
        { name: 'assigned_at', label: 'Assigned At', type: 'datetime-local', required: true },
      ],
      endpoint: 'assignments',
    },
  };
  