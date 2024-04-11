from flask import Blueprint, jsonify 

from flask_wtf.csrf import generate_csrf

from api import db, bcrypt
from api.models import AudioFile

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Welcome to Flask App!"

@main.route('/csrf-token')
def csrf_token():
    return jsonify({'csrf_token': generate_csrf()})

@main.route('/print_db')
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
