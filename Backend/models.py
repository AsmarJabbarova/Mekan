from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint
from werkzeug.security import generate_password_hash
import os

db = SQLAlchemy()

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    drivers = db.relationship('Driver', back_populates='company', lazy=True)


class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    drivers = db.relationship('Driver', back_populates='languages', lazy=True)
    user_preferences = db.relationship('UserPreference', back_populates='language', lazy=True)
    place_translations = db.relationship('PlaceTranslation', back_populates='language', lazy=True)


class EntertainmentType(db.Model):
    __tablename__ = 'entertainment_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    places = db.relationship('Place', back_populates='entertainment_type', lazy=True)
    user_preferences = db.relationship('UserPreference', back_populates='entertainment_type', lazy=True)


class PlaceCategory(db.Model):
    __tablename__ = 'place_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    places = db.relationship('Place', back_populates='category', lazy=True)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False, index=True)
    email = db.Column(db.String(40), unique=True, nullable=False, index=True)
    phone_number = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    password_salt = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    status = db.Column(db.Enum('active', 'inactive', 'suspended'), default='active')
    last_online = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    favourite_places = db.Column(db.JSON)
    audits = db.relationship('UserAudit', back_populates='user', lazy=True)
    sessions = db.relationship('UserSession', back_populates='user', lazy=True)
    bookings = db.relationship('Booking', back_populates='user', lazy=True)
    reviews = db.relationship('Review', back_populates='user', lazy=True)
    preferences = db.relationship('UserPreference', back_populates='user', lazy=True)

    def set_password(self, password):
        """Hashes the password and stores the salt and hash."""
        salt = os.urandom(16)
        self.password_salt = salt.hex()
        self.password_hash = generate_password_hash(password + self.password_salt, method='pbkdf2:sha256')

    def check_password(self, password):
        """Checks if the given password matches the stored hash."""
        return self.password_hash == generate_password_hash(password + self.password_salt, method='pbkdf2:sha256')


class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    preferred_entertainment_type = db.Column(db.Integer, db.ForeignKey('entertainment_types.id'))
    preferred_rating_range = db.Column(db.String(20))
    preferred_language = db.Column(db.Integer, db.ForeignKey('languages.id'))
    preferred_location = db.Column(db.String(40))
    preferred_price_range = db.Column(db.String(20))
    user = db.relationship("User", back_populates="preferences", lazy=True)
    entertainment_type = db.relationship("EntertainmentType", back_populates="user_preferences", lazy=True)
    language = db.relationship("Language", back_populates="user_preferences", lazy=True)
    __table_args__ = (
        CheckConstraint("preferred_rating_range IN ('1-2', '2-3', '3-4', '4-5')", name='check_preferred_rating_range'),
        CheckConstraint("preferred_price_range IN ('low', 'medium', 'high')", name='check_preferred_price_range'),
        {'extend_existing': True}
    )


class UserAudit(db.Model):
    __tablename__ = 'user_audits'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    changed_data = db.Column(db.JSON)
    action_timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user = db.relationship('User', back_populates='audits', lazy=True)


class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True)
    login_timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    logout_timestamp = db.Column(db.DateTime)
    user = db.relationship('User', back_populates='sessions', lazy=True)


class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(40))
    latitude = db.Column(db.Numeric(9, 6))
    longitude = db.Column(db.Numeric(9, 6))
    rating = db.Column(db.Float, nullable = False)
    entertainment_type_id = db.Column(db.Integer, db.ForeignKey('entertainment_types.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('place_categories.id'))
    default_price = db.Column(db.Numeric(10, 2))
    images = db.Column(db.JSON, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    entertainment_type = db.relationship('EntertainmentType', back_populates='places', lazy=True)
    category = db.relationship('PlaceCategory', back_populates='places', lazy=True)
    bookings = db.relationship('Booking', back_populates='place', lazy=True)
    pricing_rules = db.relationship('PricingRule', back_populates='place', lazy=True)
    promotions = db.relationship('Promotion', back_populates='place', lazy=True)
    assignments = db.relationship('Assignment', back_populates='place', lazy=True)
    availabilities = db.relationship('Availability', back_populates='place', lazy=True)
    reviews = db.relationship('Review', back_populates='place', lazy=True)
    translations = db.relationship('PlaceTranslation', back_populates='place', lazy=True)
    origin_routes = db.relationship('Transportation', foreign_keys='Transportation.origin_place_id', back_populates='origin_place', lazy=True)
    destination_routes = db.relationship('Transportation', foreign_keys='Transportation.destination_place_id', back_populates='destination_place', lazy=True)
    __table_args__ = (
        CheckConstraint('rating BETWEEN 1 AND 5', name='check_rating_between_1_and_5'),
    )


class PricingRule(db.Model):
    __tablename__ = 'pricing_rules'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    rule_type = db.Column(db.Enum('seasonal', 'dynamic', 'discount'), nullable=False)
    rule_conditions = db.Column(db.JSON)
    price_modifier = db.Column(db.Float)
    rule_start = db.Column(db.DateTime)
    rule_end = db.Column(db.DateTime)
    place = db.relationship('Place', back_populates='pricing_rules', lazy=True)


class Promotion(db.Model):
    __tablename__ = 'promotions'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    discount_type = db.Column(db.Enum('percentage', 'fixed_amount'))
    value = db.Column(db.Float)
    min_purchase_amount = db.Column(db.Numeric(10, 2))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    place = db.relationship('Place', back_populates='promotions', lazy=True)


class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    age = db.Column(db.Integer)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    status = db.Column(db.Enum('available', 'unavailable'), default='available')
    assignments = db.relationship('Assignment', back_populates='driver', lazy=True)
    company = db.relationship('Company', back_populates='drivers', lazy=True)
    languages = db.relationship('Language', back_populates='drivers', lazy=True)
    bookings = db.relationship('Booking', back_populates='driver', lazy=True)


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    driver = db.relationship('Driver', back_populates='assignments', lazy=True)
    place = db.relationship('Place', back_populates='assignments', lazy=True)


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'))
    booking_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    status = db.Column(db.Enum('pending', 'confirmed', 'cancelled'), default='pending')
    total_cost = db.Column(db.Numeric(10, 2))
    pricing_snapshot = db.Column(db.JSON)
    payment_status = db.Column(db.Enum('unpaid', 'paid', 'refunded'), default='unpaid')
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    transactions = db.relationship('BookingTransaction', back_populates='booking', lazy=True)
    payments = db.relationship('Payment', back_populates='booking', lazy=True)
    emergency_contacts = db.relationship('EmergencyContact', back_populates='booking', lazy=True)
    user = db.relationship("User", back_populates="bookings", lazy=True)
    place = db.relationship("Place", back_populates="bookings", lazy=True)
    driver = db.relationship("Driver", back_populates="bookings", lazy=True)


class BookingTransaction(db.Model):
    __tablename__ = 'booking_transactions'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'completed', 'failed'), nullable=False)
    amount = db.Column(db.Numeric(10, 2))
    transaction_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    booking = db.relationship("Booking", back_populates="transactions", lazy=True)


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum('credit_card', 'paypal', 'bank_transfer'))
    transaction_status = db.Column(db.Enum('completed', 'pending', 'failed'))
    transaction_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    booking = db.relationship("Booking", back_populates="payments", lazy=True)
    currency = db.relationship("Currency", back_populates="payments", lazy=True)

class Currency(db.Model):
    __tablename__ = 'currencies'
    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String(3), unique=True, nullable=False)
    symbol = db.Column(db.String(5))
    exchange_rate = db.Column(db.Float)
    is_default = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    payments = db.relationship('Payment', back_populates='currency', lazy=True)


class Availability(db.Model):
    __tablename__ = 'availabilities'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    entity_id = db.Column(db.Integer)
    entity_type = db.Column(db.Enum('driver', 'place'), nullable=False)
    availability_start = db.Column(db.DateTime)
    availability_end = db.Column(db.DateTime)
    place = db.relationship("Place", back_populates="availabilities", lazy=True)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text)
    publish_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    media = db.relationship('ReviewMedia', back_populates='review', lazy=True)
    place = db.relationship("Place", back_populates="reviews", lazy=True)
    user = db.relationship("User", back_populates="reviews", lazy=True)
    __table_args__ = (
        CheckConstraint('rating BETWEEN 1 AND 5', name='check_rating_between_1_and_5'),
    )


class ReviewMedia(db.Model):
    __tablename__ = 'review_medias'
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    media_url = db.Column(db.String(255))
    media_type = db.Column(db.Enum('image', 'video'))
    upload_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    review = db.relationship("Review", back_populates="media", lazy=True)


class Transportation(db.Model):
    __tablename__ = 'transportations'
    id = db.Column(db.Integer, primary_key=True)
    origin_place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    destination_place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    transport_type = db.Column(db.String(20))
    duration = db.Column(db.Integer)
    cost = db.Column(db.Numeric(10, 2))
    segments = db.relationship('RouteSegment', back_populates='transportation', lazy=True)
    origin_place = db.relationship("Place", back_populates="origin_routes", lazy=True, foreign_keys=[origin_place_id])
    destination_place = db.relationship("Place", back_populates="destination_routes", lazy=True, foreign_keys=[destination_place_id])


class PlaceTranslation(db.Model):
    __tablename__ = 'place_translations'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)
    translated_name = db.Column(db.String(40))
    translated_description = db.Column(db.Text)
    place = db.relationship("Place", back_populates="translations", lazy=True)
    language = db.relationship("Language", back_populates="place_translations", lazy=True)


class EmergencyContact(db.Model):
    __tablename__ = 'emergency_contacts'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    name = db.Column(db.String(40))
    phone_number = db.Column(db.String(20))
    relation = db.Column(db.String(20))
    booking = db.relationship("Booking", back_populates="emergency_contacts", lazy=True)


class RouteSegment(db.Model):
    __tablename__ = 'route_segments'
    id = db.Column(db.Integer, primary_key=True)
    transportation_id = db.Column(db.Integer, db.ForeignKey('transportations.id'), nullable=False)
    origin_place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    destination_place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    segment_order = db.Column(db.Integer, nullable=False)
    distance_km = db.Column(db.Numeric(10, 2))
    duration_minutes = db.Column(db.Integer)
    transport_mode = db.Column(db.Enum('bus', 'train', 'car', 'plane', 'boat', 'walking'))
    transportation = db.relationship("Transportation", back_populates="segments", lazy=True)
