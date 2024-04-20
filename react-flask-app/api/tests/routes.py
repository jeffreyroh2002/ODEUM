from api import db

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user 

from ..main import NUM_AUDIO

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
        test = Test.query.filter_by(user_id=user.id, test_type=1).order_by(Test.test_start_time.desc()).first()
        audio_id = 1
    else:
        last_answer = UserAnswer.query.filter(UserAnswer.test_id==test.id, UserAnswer.overall_rating != None) \
                                      .order_by(UserAnswer.audio_id.desc()).first()
        audio_id = (1 if last_answer == None else last_answer.audio_id)  

        

    return jsonify({
                'status': 'in_progress',
                'audio_id': audio_id,
                'test_id': test.id
    })


@tests.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    
    #saving answer data
    audio_id = int(data['audio_id'])
    rating = data['rating']
    question_index = data['question_index']
    test_id = int(data['test_id'])
    #saving to database
    answer = UserAnswer.query.filter_by(test_id=test_id, audio_id=audio_id, question_index=question_index).first()
    if not answer:
        new_answer = UserAnswer(audio_id=audio_id, test_id=test_id, user_id=current_user.id, question_index=question_index)
        db.session.add(new_answer)
        db.session.commit()
        answer = UserAnswer.query.filter_by(audio_id=audio_id, test_id=test_id, user_id=current_user.id).first()
    answer.overall_rating = rating
    db.session.commit()
    answer = UserAnswer.query.filter_by(question_index=question_index, test_id=test_id, user_id=current_user.id).first()
    print("submitted answer", answer, "of questionIndex", question_index)
    #if this is the last question, record the test end time
    if audio_id == NUM_AUDIO:
        test = Test.query.get(test_id)
        test.test_end_time = datetime.now()
        db.session.commit()
    

    return jsonify({"Hello": "World"})

@tests.route('/get_next_audio_id', methods=['GET'])
@login_required
def get_next_audio_id():
    test_id = int(request.args.get('test_id'))
    question_index = int(request.args.get('question_index'))
    current_answer = UserAnswer.query.filter_by(test_id=test_id, question_index=question_index).first()
    if current_answer.question_index == NUM_AUDIO - 1:
        next_audio_id = 0
        next_audio_name = ''
    else:
        next_audio_id = current_answer.audio_id + 1
        dir_path = "/workspace/ODEUM/react-flask-app/api/static/audio_files"
        filenames = os.listdir(dir_path)
        full_filenames = ['static/audio_files/' + filename for filename in filenames]       
        next_audio_name = full_filenames[int(next_audio_id) - 1]


    # next_answer = UserAnswer.query.filter_by(test_id=test_id, audio_id=next_audio_id)
    # if not next_answer:
    #     next_answer = UserAnswer(user_id=current_user.id, audio_id=next_audio_id, test_id=test_id, question_index=question_index+1)
    #     db.session.add(next_answer)
    #     db.session.commit()

    return jsonify({"next_audio_id": next_audio_id, "next_audio_name": next_audio_name})   
    
@tests.route('/get_prev_audio_id', methods=['GET'])
@login_required
def get_prev_audio_id():
    test_id = int(request.args.get('test_id'))
    question_index = int(request.args.get('question_index'))

    prev_answer = UserAnswer.query.filter_by(test_id=test_id, question_index=question_index-1).first()
    print("prev_info", prev_answer.audio_id, prev_answer.overall_rating, prev_answer.question_index)
    prev_audio_id = prev_answer.audio_id
    dir_path = "/workspace/ODEUM/react-flask-app/api/static/audio_files"
    filenames = os.listdir(dir_path)
    full_filenames = ['static/audio_files/' + filename for filename in filenames]       
    prev_audio_name = full_filenames[int(prev_audio_id) - 1]

    return jsonify({"prev_audio_id": prev_audio_id, "prev_audio_name": prev_audio_name})    