import awsgi
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from services.controller import *
from configs import CONFIG as config
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = config.JWT_REFRESH_TOKEN_EXPIRES

api = Api(app)
JWTManager(app)
CORS(app, supports_credentials=True)

api.add_resource(AuthService, '/api/auth')

def handler(event, context) -> dict:
    print(event)
    return awsgi.response(app, event, context)

if __name__ == "__main__":
    app.run(port=6600, host='0.0.0.0')