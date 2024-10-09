from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config.Config')
CORS(app)
api = Api(app)
    
@app.route('/')
def home():
    return "Welcome to the API"

if __name__ == '__main__':
    app.run(debug=True)
