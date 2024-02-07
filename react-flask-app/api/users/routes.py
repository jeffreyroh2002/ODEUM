from flask import Blueprint, request, jsonify
from flask_login import current_user
from api import db, bcrypt
from api.models import User
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError

users = Blueprint('users', __name__)

# Assuming csrf is initialized elsewhere in your application
from api import csrf

def validate_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        raise ValidationError('That username is taken. Please choose a different one.')

def validate_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        raise ValidationError('That email is taken. Please choose a different one.')

@users.route("/register", methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify({'error': 'User is already authenticated'}), 400

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    try:
        # Manual validations
        if not username or not email or not password or not confirm_password:
            raise ValidationError('All fields are required.')
        validate_username(username)
        validate_email(email)
        if password != confirm_password:
            raise ValidationError('Passwords must match.')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # Response with CSRF token if needed for subsequent requests
        csrf_token = csrf.generate_csrf()
        return jsonify({'message': 'Your account has been created!', 'csrf_token': csrf_token}), 201

    except ValidationError as e:
        return jsonify({'error': str(e)}), 400