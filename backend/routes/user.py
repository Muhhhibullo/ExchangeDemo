from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from database.db_config import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

# Protect profile route with JWT authentication
@user_bp.route('/profile', methods=['GET'])
@jwt_required()  # Ensures that the user is logged in
def get_profile():
    user_id = get_jwt_identity()  # Get the user ID from the JWT
    user = User.query.get(user_id)  # Query the user by ID
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({"username": user.username, "email": user.email}), 200


# SignUp route for new users
@user_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')  # Get confirm_password from the request

        # Check for missing fields
        if not username or not email or not password or not confirm_password:
            return jsonify({"message": "All fields are required"}), 400

        # Validate if password and confirm_password match
        if password != confirm_password:
            return jsonify({"message": "Passwords do not match"}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')

        # Create the new user
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


# Login route
@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "All fields are required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"message": "Invalid credentials"}), 401

        # Create JWT token
        token = create_access_token(identity=user.id)
        return jsonify({"token": token}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
