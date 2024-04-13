from flask import Flask, Blueprint, request, redirect, session, url_for, current_app, jsonify
import requests
import os
import base64

presurvey = Blueprint('presurvey', __name__)

questions = [
    {
        "id": 1,
        "text": "Are you aware of your musical preferences?",
        "answers": ["Yes", "No"]
    },
    {
        "id": 2,
        "text": "Would you like to discover new music or find tracks similar to what you already enjoy?",
        "answers": ["Explore new style of music", "Find similar music to my current favorites"]
    },
    {
        "id": 3,
        "text": "What genres of music do you prefer?",
        "answers": ["Pop", "Rock", "Hip-Hop", "Jazz", "Electronic", "R&B", "Indie"]
    },
    {
        "id": 4,
        "text": "Do you listen to music based on specific contexts or situations, or more casually?",
        "answers": ["Based on contexts or situations", "More casual"]
    }
]

@presurvey.route('/get_presurvey_questions', methods=['GET'])
def get_presurvey_questions():
    return jsonify(questions)

@presurvey.route('/process_presurvey_questions', methods=['POST'])
def process_presurvey_questions():
    data = request.get_json()
    print(f"Received answer for question {data['questionId']}: {data['answer']}")
    # Here you might want to save the answer to a database or perform some processing
    return jsonify({"status": "success", "message": "Answer received"}), 200