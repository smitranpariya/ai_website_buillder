from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os
from app import mongo

# Create Blueprint
auth_bp = Blueprint('auth', __name__)

# Signup Route
@auth_bp.route('/signup', methods=['POST'])
def signup():
    print("✅ /api/auth/signup route HIT")

    # Get data from the request
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Debug: print the data you're trying to insert
    print(f"Trying to insert: email = {email}, password = {password}")

    # Check if user already exists
    user = mongo.users.find_one({"email": email})
    if user:
        print(" User already exists!")
        return jsonify({"msg": "User already exists"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Insert into DB
    result = mongo.users.insert_one({
        "email": email,
        "password": hashed_password
    })

    # Debug: check if insertion was successful
    print("Inserted user ID:", result.inserted_id)

    return jsonify({"msg": "User created successfully"}), 201


# Login Route
@auth_bp.route('/login', methods=['POST'])
def login():
    # Get data from request body
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    # Check if the user exists
    user = mongo.users.find_one({"email": email})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"msg": "Invalid credentials"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=user['email'])
    return jsonify(access_token=access_token), 200

@auth_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def profile():
    current_user_email = get_jwt_identity()

    # Fetch user details from MongoDB (you can customize this)
    user = mongo.users.find_one({"email": current_user_email}, {"_id": 0, "password": 0})  # exclude sensitive data
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({"user": user}), 200