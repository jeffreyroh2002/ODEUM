from flask import Flask, Blueprint, request, redirect, session, url_for, current_app, jsonify
import requests
import os
import base64

presurvey = Blueprint('presurvey', __name__)

questions = [
    {
        "id": 1,
        "text": "What is your favorite color?",
        "answers": ["Red", "Blue", "Green", "Yellow"]
    },
    {
        "id": 2,
        "text": "What is your preferred pet?",
        "answers": ["Dog", "Cat", "Bird", "Fish"]
    }
]

@presurvey.route('/get_presurvey_questions', methods=['GET'])
def get_presurvey_questions():
    return jsonify(questions)

@app.route('/process_presurvey_questions', methods=['POST'])
def process_presurvey_questions():
    data = request.get_json()
    print(f"Received answer for question {data['questionId']}: {data['answer']}")
    # Here you might want to save the answer to a database or perform some processing
    return jsonify({"status": "success", "message": "Answer received"}), 200