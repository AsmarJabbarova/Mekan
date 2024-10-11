from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20))
    last_online = db.Column(db.DateTime)
    reviews = db.relationship('Review', backref='user', lazy=True)
    audits = db.relationship('UsersAudit', backref='user', lazy=True)

class UsersAudit(db.Model):
    __tablename__ = 'users_audit'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(20))
    changed_data = db.Column(db.JSON)
    action_timestamp = db.Column(db.DateTime)

class EntertainmentType(db.Model):
    __tablename__ = 'entertainment_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    location = db.Column(db.String(40))
    rating = db.Column(db.Float)
    entertainment_type_id = db.Column(db.Integer, db.ForeignKey('entertainment_types.id'))

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Float)
    comment = db.Column(db.Text)
    publish_date = db.Column(db.DateTime)

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    name = db.Column(db.String(40))
    surname = db.Column(db.String(40))
    age = db.Column(db.Integer)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    status = db.Column(db.String(20))

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    assigned_at = db.Column(db.DateTime)
