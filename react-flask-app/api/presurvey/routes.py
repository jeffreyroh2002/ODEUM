from flask import Flask, Blueprint, request, redirect, session, url_for, current_app, jsonify
from api import db, login_manager
from api.models import User, AudioFile, UserAnswer, Test
import requests
import os
import base64
import json
from flask_login import login_required, current_user 


presurvey = Blueprint('presurvey', __name__)

questions = [
    {
        "id": 1,
        "text": "Are you aware of your musical preferences?",
        "answers": ["Yes", "No"],
        "allow_multiple": False
    },
    {
        "id": 2,
        "text": "Would you like to discover new music or find tracks similar to what you already enjoy?",
        "answers": ["Explore new style of music", "Find similar music to my current favorites"],
        "allow_multiple": False
    },
    {
        "id": 3,
        "text": "What genres of music do you prefer?",
        "answers": ["Pop", "Rock", "Hip-Hop", "Jazz", "Electronic", "R&B", "Indie"],
        "allow_multiple": True
    },
    {
        "id": 4,
        "text": "Do you listen to music based on specific contexts or situations, or more casually?",
        "answers": ["Based on contexts or situations", "More casual"],
        "allow_multiple": False
    }
]

@presurvey.route('/get_presurvey_questions', methods=['GET'])
def get_presurvey_questions():
    return jsonify(questions)

@presurvey.route('/process_presurvey_questions', methods=['POST'])
@login_required
def process_presurvey_questions():
    if request.method == 'POST':
        data = request.get_json()
        question_id = data.get('questionId')
        answers = data.get('answers', [])
        print("here are the answers from frontend:", answers)
        # Fetch the most recent test for the current user
        test = Test.query.filter_by(user_id=current_user.id).order_by(Test.test_start_time.desc()).first()
        
        if test is not None:
            # Assuming pre_survey_data is a JSON-formatted text field that needs to be updated
            if test.pre_survey_data:
                # Decode existing answers if available
                existing_answers = json.loads(test.pre_survey_data)
            else:
                existing_answers = {}
            
            # Update the answers for the specific question
            existing_answers[str(question_id)] = answers
            
            # Serialize and save back to the test
            test.pre_survey_data = json.dumps(existing_answers)
            db.session.commit()
            print("Here is what is commited to DB!!!:", test.pre_survey_data)
            return jsonify({"message": "Pre-survey answers updated successfully!", "test_id": test.id}), 200
        else:
            return jsonify({"error": "No test found for the user"}), 404
    else:
        return jsonify({"error": "Method not allowed"}), 405