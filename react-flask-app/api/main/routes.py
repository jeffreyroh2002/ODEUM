from flask import Blueprint, jsonify, request, session
from api import db, bcrypt
from api.models import User
from api.models import AudioFile
from api.users.forms import RegistrationForm, LoginForm, UpdateAccountForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return("Welcome to Flask App!")

@main.route('/printdb')
def get_database():
    # Query all AudioFile objects from the database
    audio_files = AudioFile.query.all()

    # Prepare a list to store the serialized data
    serialized_audio_files = []

    # Serialize each AudioFile object
    for audio_file in audio_files:
        serialized_audio_files.append({
            'audio_name': audio_file.audio_name,
            'file_path': audio_file.file_path,
            'genre': audio_file.genre,
            'mood': audio_file.mood,
            'vocal': audio_file.vocal
        })

    # Return the serialized data as a JSON response
    return jsonify(serialized_audio_files)

@main.route('/signup', methods=["POST"])
def signup():
    first_name = request.json['first_name']
    email = request.json['email']
    password = request.json['password']
    confirm_password = request.get['confirmed_password']

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "Email already exists"}), 409
    
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

@main.route('/login', methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized Access"}), 401
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    session["user_id"] = user.itsdangerous
    
    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "email:" user.email
    })