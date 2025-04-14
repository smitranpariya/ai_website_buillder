from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address)

# Load environment variables
load_dotenv()
cache = Cache()

# Global DB variable (actual database, not client)
mongo = None
jwt = JWTManager()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config['CACHE_TYPE'] = 'SimpleCache'  # You can switch to Redis or Memcached in production
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes

    cache.init_app(app)
    limiter.init_app(app)

    CORS(app)
    jwt.init_app(app)

    # Parse DB name from URI
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db_name = mongo_uri.rsplit('/', 1)[-1]  # Extract db name from URI
    global mongo
    mongo = client[db_name]
    print("Connected to MongoDB:", mongo.name)  # Set global mongo to the database object

    # Register blueprints
    from app.auth import auth_bp
    from app.ai import ai_bp
    from app.website import website_bp
    from .routes import pages
    from app.preview import preview_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(website_bp, url_prefix='/api/website')
    app.register_blueprint(preview_bp, url_prefix='/api')
    app.register_blueprint(pages)

    return app


