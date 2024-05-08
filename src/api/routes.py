"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required


# app = Flask(__name__)

api = Blueprint('api', __name__)

# Allow CORS requests to this API
# CORS(api)


# @api.route('/signup', methods=['POST'])
# def new_user():

#     response_body = {
#         "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
#     }

#     return jsonify(response_body), 200
    
@api.route('/user/signup', methods=['POST'])
def sign_up():
    new_email = request.json.get("email", None)
    new_password = request.json.get("password", None)

    user = User(password = new_password, email = new_email)
    db.session.add(user)
    db.session.commit()

@api.route('/token', methods=['POST'])
def create_token():
    email = request.json.get("email", None)
    # password = request.json.get("password", None)
    # if email != "test" or password != "test":
    #     return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

@api.route('/user/private_page', methods=['GET'])
@jwt_required()
def log_in():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    return jsonify({"id": user.id, "username": user.username }), 200

