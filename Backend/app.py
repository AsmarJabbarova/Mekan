from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from flask_restx import Api
from flask_migrate import Migrate
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
from flask_caching import Cache
from logging.config import dictConfig
from dotenv import load_dotenv
from datetime import timedelta
from models import db, User
from db import close_db_connection
from resources.users import UsersResource, UserResource
from resources.users_audits import UsersAuditResource
from resources.entertainment_types import EntertainmentTypesResource, EntertainmentTypeResource
from resources.places import PlacesResource, PlaceResource
from resources.reviews import ReviewsResource, ReviewResource
from resources.companies import CompaniesResource, CompanyResource
from resources.languages import LanguagesResource, LanguageResource
from resources.drivers import DriversResource, DriverResource
from resources.assignments import AssignmentsResource, AssignmentResource
from resources.login import UserLogin, UserLogout
from resources.bookings import BookingsResource, BookingResource
from resources.payments import PaymentsResource, PaymentResource
from resources.transportations import TransportationsResource, TransportationResource
from resources.user_preferences import UserPreferencesResource, UserPreferenceResource
from resources.user_sessions import UserSessionsResource, UserSessionResource
import os

# Role-based access control decorator
def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] != role:
                return jsonify(message="Permission denied"), 403
            return fn(*args, **kwargs)
        return inner
    return wrapper

# Initializing the Flask app
app = Flask(__name__)

# Initialize Redis client
redis_client = Redis(
    host='localhost',
    port=6379,
    db=0
)

redis_client.ping()

# Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day"],
    storage_uri="redis://localhost:6379"
)

# Index route
@app.route('/')
@limiter.limit("5 per minute")
def index():
    return "Welcome to the API !"

# Load environment variables from .env
load_dotenv()


# Database, JWT and Migration setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'mysql+pymysql://root:@localhost/mekan')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'e607fabba6613e1a5d00bb5edcc929ac213c494de724ad2d')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)

db.init_app(app)
migrate = Migrate(app, db)

# Setting up logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'file_handler']
    }
})

# App environment configuration
env = os.getenv('FLASK_ENV', 'development')
if env == 'development':
    app.config.from_object('config.development.Config')
else:
    app.config.from_object('config.production.Config')

# CORS, Cache
CORS(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
rest_api = Api(app, doc='/docs', title='Tourism Project API', description='API documentation for Tourism Project')

# Error handling
@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify(error="You have exceeded your rate limit. Please try again later."), 429

@app.errorhandler(500)
@jwt_required()
def internal_error(error):
    app.logger.error(f"Server Error: {error} | Request: {request.method} {request.url} | User: {get_jwt_identity()}")
    return jsonify(error="Internal server error. Please try again later."), 500

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error('Not Found: %s', (error))
    return jsonify(error="Resource not found. Please check the URL and try again."), 404

# Registering resources
rest_api.add_resource(UsersResource, '/users')
rest_api.add_resource(UserResource, '/users/<int:user_id>')
rest_api.add_resource(UserLogin, '/login')
rest_api.add_resource(UserLogout, '/logout')
rest_api.add_resource(UsersAuditResource, '/users_audit')
rest_api.add_resource(EntertainmentTypesResource, '/entertainment_types')
rest_api.add_resource(EntertainmentTypeResource, '/entertainment_types/<int:entertainment_type_id>')
rest_api.add_resource(PlacesResource, '/places')
rest_api.add_resource(PlaceResource, '/places/<int:place_id>')
rest_api.add_resource(ReviewsResource, '/reviews')
rest_api.add_resource(ReviewResource, '/reviews/<int:review_id>')
rest_api.add_resource(CompaniesResource, '/companies')
rest_api.add_resource(CompanyResource, '/companies/<int:company_id>')
rest_api.add_resource(LanguagesResource, '/languages')
rest_api.add_resource(LanguageResource, '/languages/<int:language_id>')
rest_api.add_resource(DriversResource, '/drivers')
rest_api.add_resource(DriverResource, '/drivers/<int:driver_id>')
rest_api.add_resource(AssignmentsResource, '/assignments')
rest_api.add_resource(AssignmentResource, '/assignments/<int:assignment_id>')
rest_api.add_resource(BookingsResource, '/bookings')
rest_api.add_resource(BookingResource, '/bookings/<int:booking_id>')
rest_api.add_resource(PaymentsResource, '/payments')
rest_api.add_resource(PaymentResource, '/payments/<int:payment_id>')
rest_api.add_resource(TransportationsResource, '/transportations')
rest_api.add_resource(TransportationResource, '/transportations/<int:transportation_id>')
rest_api.add_resource(UserPreferencesResource, '/user_preferences')
rest_api.add_resource(UserPreferenceResource, '/user_preferences/<int:preference_id>')
rest_api.add_resource(UserSessionsResource, '/user_sessions')
rest_api.add_resource(UserSessionResource, '/user_sessions/<int:session_id>')

@app.before_request
def log_request_info():
    app.logger.info(f"Request: {request.method} {request.url} | Body: {request.get_data()}")

@app.teardown_appcontext
def teardown_db(exception):
    close_db_connection()

# Admin route
@app.route('/admin', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_dashboard():
    return jsonify(message="Welcome, Admin!")

#Listing all routes route
@app.route('/routes')
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote(f"{rule.endpoint}: {methods} {rule}")
        output.append(line)
    return jsonify(output)

# Refresh route
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh = True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200

# with app.app_context():
    # db.create_all()
    # user = User(username="user0", email="user0@postman.com")
    # user.set_password("user0_password")
    # db.session.add(user)
    # db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
