"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask_cors import CORS
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from flask_jwt_extended import JWTManager

# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")
jwt = JWTManager(app)

# # !!!!! My added code->
# def token_required(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         token = request.args.get('token')
#         if not token:
#             return jsonify({'Alert!': 'Token is missing!'})
#         try:
#             payload = jwt.decode(token, app.config['SECRET_KEY'])
#         except:
#             return jsonify({'Alert!': 'Invalid Token!'})
#         return decorated
# # -> My added code

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

CORS(app)


# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file


@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response

# !!!!! My added code !!!!!
# @app.route('/login', methods=['POST'])
# def login():
#     if request.form['username'] and request.form['password'] == '123456':
#         session['logged in'] = True
#         token = jwt.encode({
#         'user':request.form['username'],
#         'expiration': str(datetime.utcnow() + timedelta(seconds=300))
#         },
#             app.config['SECRET_KEY'])
#         return jsonify({'token': token.decode('utf-8')})
#     else:
#         return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm:"Authentication Failed!'})


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
