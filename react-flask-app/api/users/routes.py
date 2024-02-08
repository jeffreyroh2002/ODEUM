
from flask import jsonify, request, Blueprint
from api import db, bcrypt
from api.models import User

users = Blueprint('users', __name__)

@users.route("/users/register", methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    # Validate input
    if not username or not email or not password or not confirm_password:
        return jsonify({"error": "All fields are required"}), 400
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create user
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201

@users.route("/users/login", methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Log in user (you need to implement your login mechanism)
    # login_user(user)

    return jsonify({"message": "Login successful"}), 200

@users.route("/users/logout", methods=['POST'])
def logout():
    # Implement your logout mechanism here
    return jsonify({"message": "Logout successful"}), 200

@users.route("/users/account", methods=['GET', 'PUT'])
def account():
    if request.method == 'PUT':
        data = request.get_json()
        # Update account details (you need to implement this logic)
        return jsonify({"message": "Account updated"}), 200
    elif request.method == 'GET':
        # Get account details (you need to implement this logic)
        return jsonify({"message": "Get account details"}), 200

@users.route("/users/mypage", methods=['GET'])
def mypage():
    # Return user's page (you need to implement this logic)
    return jsonify({"message": "My Page"}), 200
