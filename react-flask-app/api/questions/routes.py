from flask import Blueprint, jsonify, request
from flask_login import login_required

from ..models import UserAnswer, Test, AudioFile

import os

questions = Blueprint("questions", __name__)

@questions.route('/get_question_metadata', methods=['GET'])
@login_required
def get_question_metadata():
    audio_id = request.args.get('audio_id', type=int)
    dir_path = "/workspace/ODEUM/react-flask-app/api/static/audio_files"
    filenames = os.listdir(dir_path)
    full_filenames = ['static/audio_files/' + filename for filename in filenames]
    return jsonify({"audio_filename": full_filenames[int(audio_id) - 1]})


@login_required
@questions.route('/get_useranswer', methods=['GET'])
def get_useranswer():
    audio_id = int(request.args.get('audio_id'))
    test_id = int(request.args.get('test_id'))
    
    answer = UserAnswer.query.filter_by(test_id=test_id, audio_id=audio_id).first()
    rating = (getattr(answer, 'overall_rating') if answer else None)
    return jsonify({"rating" : rating})


def get_next_audio_file_id(current_audio_file_id):
    # Query for the next AudioFile ID greater than the current one
    next_audio_file = AudioFile.query.filter(AudioFile.id > current_audio_file_id).order_by(AudioFile.id).first()
    return next_audio_file.id if next_audio_file else None

def get_prev_audio_file_id(current_audio_file_id):
    # Query for the previous AudioFile ID less than the current one
    prev_audio_file = AudioFile.query.filter(AudioFile.id < current_audio_file_id).order_by(AudioFile.id.desc()).first()
    return prev_audio_file.id if prev_audio_file else None

@login_required
@questions.route('/get_next_questions', methods=["GET"])
def get_next_questions():
    test_type = request.args.get('test_type', type=int)
    audio_file_id = request.args.get('audio_file_id', type=int)
    test_id = request.args.get('test_id', type=int)

    if not test_type or audio_file_id is None:
        return jsonify({'error': 'Missing required parameters'}), 400

    user = current_user

    # Find the latest test of the specified type for the user
    test = Test.query.filter_by(user_id=user.id, test_type=test_type, id=test_id).first()
    # Continue with the ongoing test
    audio_file = AudioFile.query.get(audio_file_id)
    newTest = False
    return jsonify({
                'status': 'in_progress',
                'new_test': newTest,
                'audio_file_id': audio_file_id,
                'audio_file_name': audio_file.audio_name,
                'test_id': test.id,
    })


@login_required
@questions.route('/get_prev_questions', methods=["POST"])
def get_prev_questions():

    print("inside getprevquestions!")
    data = request.json

    test_id = data['test_id']
    audio_id = data['audio_id']

    if not test_id or audio_id is None:
        return jsonify({'error': 'Missing required parameters'}), 400

    user = current_user

    # Find the latest test of the specified type for the user
    test = Test.query.filter_by(user_id=user.id, id=test_id).order_by(Test.test_start_time.desc()).first()

    # Continue with the ongoing test

    prev_audio_file_id = get_prev_audio_file_id(audio_id)

    if prev_audio_file_id != None:
        prev_audio_file = AudioFile.query.get(prev_audio_file_id)
        db_answer = UserAnswer.query.filter((UserAnswer.test == test) & (UserAnswer.audio_id == prev_audio_file.id) & (UserAnswer.user == current_user)).first()
        newTest = False

        return jsonify({
                    'status': 'in_progress',
                    'new_test': newTest,
                    'prev_audio_file_id': prev_audio_file_id,
                    'prev_audio_file_name': prev_audio_file.audio_name,
                    'test_id': test.id,
                    'overall_rating': db_answer.overall_rating,
                    'genre_rating': db_answer.genre_rating,
                    'mood_rating': db_answer.mood_rating,
                    'vocal_timbre_rating': db_answer.vocal_timbre_rating,
        })
    else:
        return jsonify({
            'status': 'send_to_before_test'
        })