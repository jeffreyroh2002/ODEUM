from api import db

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user 

from ..main import NUM_AUDIO, NUM_EXTRA_QUESTIONS, NUM_QUESTIONS_PER_AUDIO, NUM_QUESTIONS, EXTRA_QUESTIONS_INDEX, \
                   QUESTION_TYPES

from ..models import Test, UserAnswer

from datetime import datetime
import os
import json

tests = Blueprint("tests", __name__)

@tests.route('/before_test_info', methods=['GET'])
@login_required
def before_test_info():
    user = current_user
    #get the current test information
    test = Test.query.filter_by(user_id=user.id, test_type=1).order_by(Test.test_start_time.desc()).first()
    
    #if there is no test in progress, generate a new test and add to a database
    if not test or test.test_end_time:        
        test_val = Test(
            test_type = 1,
            test_start_time = datetime.now(),
            subject = user
        )
        db.session.add(test_val)
        db.session.commit()
        question_index = 1
        test = Test.query.filter_by(user_id=user.id, test_type=1).order_by(Test.test_start_time.desc()).first()

    else:
        last_answer = UserAnswer.query.filter(UserAnswer.test_id==test.id, UserAnswer.overall_rating != None) \
                                      .order_by(UserAnswer.audio_id.desc()).first()
        question_index = 1

        if last_answer != None:
            #finding the question index
            allocated_number = 1
            while True:
                if question_index not in EXTRA_QUESTIONS_INDEX:
                    if allocated_number == (last_answer.audio_id - 1) * NUM_QUESTIONS_PER_AUDIO + 1:
                        break
                    allocated_number += 1
                question_index += 1

    return jsonify({
                'status': 'in_progress',
                'question_index': question_index,
                'test_id': test.id
    })

@tests.route('/get_question_metadata', methods=['GET'])
@login_required
def get_question_metadata():
    question_index = request.args.get('question_index', type=int)
    
    if question_index in EXTRA_QUESTIONS_INDEX:
        question_type = 'additional'
    
    else:
        additional_q_before = [index for index in EXTRA_QUESTIONS_INDEX if index < question_index]
        num_additional_q_before = len(additional_q_before)
        question_index_except_additional = question_index - num_additional_q_before      
        question_type = QUESTION_TYPES[question_index % NUM_QUESTIONS_PER_AUDIO]
        audio_id = (question_index_except_additional - 1) // NUM_QUESTIONS_PER_AUDIO + 1

        dir_path = "/workspace/ODEUM/react-flask-app/api/static/audio_files"
        filenames = os.listdir(dir_path)
        full_filenames = ['static/audio_files/' + filename for filename in filenames]

    return jsonify({"question_type" : question_type, "audio_id" : audio_id,
                    "audio_filename": full_filenames[int(audio_id) - 1]})


@tests.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    
    #saving answer data
    question_index = int(data['question_index'])
    answer_type = data['type']
    audio_id = int(data['audio_id'])
    rating = int(data['rating'])
    test_id = int(data['test_id'])

    #saving to database
    answer = UserAnswer.query.filter_by(test_id=test_id, audio_id=audio_id).first()
    if answer_type == 'overall_rating' and not answer:
        new_answer = UserAnswer(audio_id=audio_id, test_id=test_id, user_id=current_user.id)
        db.session.add(new_answer)
        db.session.commit()
        answer = UserAnswer.query.filter_by(audio_id=audio_id, test_id=test_id, user_id=current_user.id).first()

    setattr(answer, answer_type, rating)
    db.session.commit()
    answer = UserAnswer.query.filter_by(test_id=test_id, audio_id=audio_id).first()

    #if this is the last question, record the test end time
    if question_index == NUM_QUESTIONS:
        test = Test.query.get(test_id)
        test.test_end_time = datetime.now()
        db.session.commit()
        
    return jsonify({"Hello": "World"})