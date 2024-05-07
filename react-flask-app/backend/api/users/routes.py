from flask import Blueprint, jsonify, request, session
from flask_login import current_user, login_required, login_user, logout_user

import re  #for signup validation

from api import db, bcrypt
from api.models import User, Test 

users = Blueprint('users', __name__)

@users.route('/signup', methods=["POST"])
def signup():
    data = request.json
    # Validate input fields (instead of form.validate_on_submit())
    if not data['first_name'] or not data['email'] or not data['password'] or not data['confirm_password']:
        
        return jsonify({"error": "Missing required field(s)!"})

    first_name = data['first_name']
    email = data['email']
    password = data['password']
    confirm_password = data['confirm_password']

     # Additional validation
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return jsonify({"error": "Invalid email format!"})

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long!"})
    
    if password != confirm_password:
        return jsonify({"error": "Password and Confirm Password do not match!"})

    user_exists = User.query.filter_by(email=email).first() is not None
    if user_exists:
        return jsonify({"error": "Email already exists!"})
    
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(first_name=first_name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id

    return jsonify({
        "id": new_user.id,
        "first_name": new_user.first_name,
        "email": new_user.email
    })

@users.route('/login', methods=["POST"])
def login():
    data = request.json

    # Validate input fields (instead of form.validate_on_submit())
    if not data['email'] or not data['password']:
        return jsonify({"error": "Missing required field(s)"})

    email = request.json["email"]
    password = request.json["password"]
    remember_me = request.json["remember_me"]

    user = User.query.filter_by(email=email).first()

    if user is None or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Check email or password"})
    
    login_user(user, remember=remember_me)
    session["user_id"] = user.id
    
    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "email": user.email
    })

@users.route('/logout', methods=["POST"])
@login_required  # Require the user to be logged in to access this route
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"})

@users.route('/is_logged_in')
def is_logged_in():
    if current_user.is_authenticated:
        return jsonify({"isLoggedIn": True})
    else:
        return jsonify({"isLoggedIn": False})
    

@login_required
@users.route('/get_user_info', methods=["GET"])
def get_user_info():
    user = current_user
    user_name = user.first_name
    tests = Test.query.filter_by(subject=current_user).order_by(Test.id.asc()).all()
    tests_data = []
    
    for test in tests:
        test_data = {
            'id': test.id,
            'test_type': test.test_type,
            'test_start_time': test.test_start_time.strftime('%Y-%m-%d %H:%M:%S'),  # Convert datetime to string
        }
        if (test.test_end_time):
            tests_data.append(test_data)

    return jsonify({
        'user_name': user_name,
        'tests_data': tests_data
    })