from flask import Flask
from flask_restful import Api
from models import db
from resources.users import UsersResource
from resources.users_audit import UsersAuditResource
from resources.entertainment_types import EntertainmentTypesResource
from resources.places import PlacesResource
from resources.reviews import ReviewsResource
from resources.companies import CompaniesResource
from resources.languages import LanguagesResource
from resources.drivers import DriversResource
from resources.assignments import AssignmentsResource
from flask_migrate import Migrate
from flask_cors import CORS
from db import close_db_connection

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)
api = Api(app)

api.add_resource(UsersResource, '/users')
api.add_resource(UsersAuditResource, '/users_audit')
api.add_resource(EntertainmentTypesResource, '/entertainment_types')
api.add_resource(PlacesResource, '/places')
api.add_resource(ReviewsResource, '/reviews')
api.add_resource(CompaniesResource, '/companies')
api.add_resource(LanguagesResource, '/languages')
api.add_resource(DriversResource, '/drivers')
api.add_resource(AssignmentsResource, '/assignments')

@app.teardown_appcontext
def teardown_db(exception):
    close_db_connection()
    
@app.route('/')
def home():
    return "Welcome to the API"

if __name__ == '__main__':
    app.run(debug=True)
