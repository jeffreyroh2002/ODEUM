from api import create_app, db

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user 


from ..models import Test, UserAnswer, AudioFile

from datetime import datetime
import os
import json
import random

from google.cloud import storage

NUM_QUESTIONS = 25

tests = Blueprint("tests", __name__)

genre_columns = ['Rock', 'Hip Hop', 'Pop Ballad', 'Electronic', 'Jazz', 'Korean Ballad', 'R&B/Soul']
mood_columns = ['Emotional', 'Tense', 'Bright', 'Relaxed']
vocal_columns = ['Smooth', 'Dreamy', 'Raspy']
columns = genre_columns + mood_columns + vocal_columns

@tests.route('/before_test_info', methods=['GET'])
@login_required
def before_test_info():
    user = current_user
    #get the current test information
    test = Test.query.filter_by(user_id=user.id).order_by(Test.test_start_time.desc()).first()
    last_answer = UserAnswer.query.filter(UserAnswer.test_id==test.id, UserAnswer.rating != None) \
                                  .order_by(UserAnswer.audio_id.desc()).first()   
    #determine the test type
    if not last_answer:
        is_aware_of_musical_taste = test.decoded_pre_survey_answers['1']
        is_discovering_new_music = test.decoded_pre_survey_answers['2']
        if is_aware_of_musical_taste == ['No']:
            test.test_type = 1
            if not test.progress: test.progress = "searching genre preference"
            db.session.commit()
            audio_id = get_next_audio_for_test_type_1(test.id, question_index = 0)
        elif is_discovering_new_music == ['Explore new style of music']:
            test.test_type = 2
            if not test.progress: test.progress = "searching genre preference"
            db.session.commit()
            audio_id = get_next_audio_for_test_type_2(test.id, question_index = 0)
        else:
            test.test_type = 3
            db.session.commit()
            audio_id = get_next_audio_for_test_type_3(test.id, question_index = 0)


        test = Test.query.filter_by(user_id=user.id).order_by(Test.test_start_time.desc()).first()
        print("test type in before test: ", test.test_type)
        print("audio id in before test: ", audio_id)

    #get existing answer info
    else:
        audio_id = last_answer.audio_id

    return jsonify({
                'status': 'in_progress',
                'audio_id': audio_id,
                'test_id': test.id,
                'test_type': test.test_type
    })


@tests.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    # loading submitted data
    data = request.data.decode('utf-8')
    data = json.loads(data)
    
    # saving answer data
    audio_id = int(data['audio_id'])
    rating = data['rating']
    question_index = data['question_index']
    test_id = int(data['test_id'])
    # getting existing useranswer
    answer = UserAnswer.query.filter_by(user_id= current_user.id, 
                                        test_id=test_id, 
                                        audio_id=audio_id, 
                                        question_index=question_index)   \
                             .first()
    # for the case when there is not an existing answer 
    if not answer:
        new_answer = UserAnswer(audio_id=audio_id, 
                                test_id=test_id, 
                                user_id=current_user.id, 
                                question_index=question_index)
        db.session.add(new_answer)
        answer = UserAnswer.query.filter_by(audio_id=audio_id, 
                                            test_id=test_id, 
                                            user_id=current_user.id, 
                                            question_index=question_index).first()

    # updating overall rating to database
    answer.rating = rating
    db.session.commit()

    # for debugging
    answer = UserAnswer.query.filter_by(question_index=question_index, 
                                        test_id=test_id, 
                                        user_id=current_user.id).first()
    print("submitted answer", answer, "of questionIndex", question_index)

    #if this is the last question, record the test end time
    if question_index == NUM_QUESTIONS:
        test = Test.query.get(test_id)
        test.test_end_time = datetime.now()
        print("test completed!!!!!!!!!!!!!!!!")
        db.session.commit()
    
    return jsonify({"Hello": "World"})

@tests.route('/get_next_audio_id', methods=['GET'])
@login_required
def get_next_audio_id():
    test_id = int(request.args.get('test_id'))
    question_index = int(request.args.get('question_index'))

    test = Test.query.get_or_404(test_id)
    #the case when the test is ended
    if question_index == NUM_QUESTIONS:
        return jsonify({"next_audio_id": 0, "next_audio_name": ''})   

    if int(test.test_type) == 1:
        next_audio_id = get_next_audio_for_test_type_1(test_id, question_index)

    elif int(test.test_type) == 2:
        next_audio_id = get_next_audio_for_test_type_2(test_id, question_index)

    else:
        next_audio_id = get_next_audio_for_test_type_3(test_id, question_index)
    
    next_audio_name = AudioFile.query.get(next_audio_id).audio_name
    
    return jsonify({"next_audio_id": next_audio_id, "next_audio_name": next_audio_name})   

    
@tests.route('/get_prev_audio_id', methods=['GET'])
@login_required
def get_prev_audio_id():
    storage_client = storage.Client(project="ODEUM-421210")
    bucket = storage_client.get_bucket("odeum-musics")
    test_id = int(request.args.get('test_id'))
    question_index = int(request.args.get('question_index'))

    prev_answer = UserAnswer.query.filter_by(test_id=test_id, question_index=question_index-1).first()
    print("prev_info", prev_answer.audio_id, prev_answer.rating, prev_answer.question_index)
    prev_audio_id = prev_answer.audio_id
    prev_audio_name = AudioFile.query.get(prev_audio_id).audio_name

    return jsonify({"prev_audio_id": prev_audio_id, "prev_audio_name": prev_audio_name})    

@login_required
@tests.route('/get_rating', methods=['GET'])
def get_rating():
    audio_id = int(request.args.get('audio_id'))
    test_id = int(request.args.get('test_id'))
    
    answer = UserAnswer.query.filter_by(user_id=current_user.id, 
                                        test_id=test_id, 
                                        audio_id=audio_id).first()
    rating = (answer.rating if answer else None)
    return jsonify({"rating" : rating})

@tests.route('/stream_audio', methods=['GET', 'POST'])
def stream_audio():
    audio_name = str(request.args.get('audio_name'))

    storage_client = storage.Client(project="ODEUM-421210")
    bucket = storage_client.get_bucket("odeum-musics")
    blob = bucket.blob("split_audio/full-audio/" + audio_name)
    print(blob.exists())
    url = blob.generate_signed_url(version="v4", expiration=3600, method="GET")
    
    return jsonify({"url":url})

@tests.route('/get_question_metadata', methods=['GET'])
@login_required
def get_question_metadata():
    audio_id = request.args.get('audio_id', type=int)
    audio_filename = AudioFile.query.get(audio_id).audio_name
    return jsonify({"audio_filename": audio_filename})

def search_audio_using_attributes(attribute, answered_audios_id):
    if attribute in genre_columns:
        attribute_type = "dominant_genre"
    elif attribute in mood_columns:
        attribute_type = "dominant_mood"
    else: attribute_type = "dominant_vocal"

    searched_answers = AudioFile.query.filter_by(**{attribute_type: attribute}).all()
    non_overlapping_answers = [answer for answer in searched_answers if answer.id not in answered_audios_id]

    return non_overlapping_answers

class NoMatchingAudioError(Exception):
    pass

def get_next_audio_for_test_type_1(test_id, question_index):
    #get existing answers data (including audio ids)
    test = Test.query.get(test_id)
    test_progress = test.progress
    answers = UserAnswer.query.filter_by(test_id=test_id).all()

    #if there is an existing answer, go to the question
    existing_next_answer = UserAnswer.query.filter_by(test_id=test_id, user_id=current_user.id, question_index=question_index+1).first()
    if existing_next_answer:
        next_audio_id = existing_next_answer.audio_id
        return next_audio_id

    answered_audios_id = [answer.audio_id for answer in answers]
    print("answered: ", answered_audios_id)
    prev_answer = UserAnswer.query.filter_by(test_id=test_id, user_id=current_user.id, question_index=question_index).first()

    #first, search the user's genre preference
    if test_progress == "searching genre preference":
        answered_audios = [AudioFile.query.get_or_404(audio_id) for audio_id in answered_audios_id]
        #randomly iterate each genre and choose one audio that contains the genre dominantly
        answered_genres = [answer.dominant_genre for answer in answered_audios]
        unanswered_genres = [genre for genre in genre_columns if genre not in answered_genres]
        print("unanswered: ", unanswered_genres)
        if not unanswered_genres:
            test_progress = "analyzing genre preference"

        else:
            next_question_genre = random.choice(unanswered_genres)
            possible_audios = search_audio_using_attributes(next_question_genre, answered_audios_id)
            if not possible_audios:
                raise NoMatchingAudioError(f'No matching audios in question index {question_index + 1} and progress {test.progress}')
            next_audio = random.choice(possible_audios)      

    if test_progress == "analyzing genre preference":
        if len(answers) == len(genre_columns):
            genre_score = {'Rock': 0, 'Hip Hop': 0, 'Pop Ballad': 0, 'Electronic': 0, 'Jazz': 0, 'Korean Ballad': 0, 'R&B/Soul': 0}
            for answer in answers:
                audio_genre = AudioFile.query.get_or_404(answer.audio_id).genre
                for genre, value in audio_genre.items():
                    genre_score[genre] += value
            preferred_genre = max(genre_score, key=genre_score.get)
            possible_audios = search_audio_using_attributes(preferred_genre, answered_audios_id)
            if not possible_audios:
                raise NoMatchingAudioError(f'No matching audios in question index {question_index + 1} and progress {test.progress}')
            next_audio = random.choice(possible_audios)       

        elif len(answers) >= len(genre_columns) + 5:
            test_progress = "analyzing additional preference"
        
        else:
            prev_audio_genre = AudioFile.query.get_or_404(prev_answer.audio_id).dominant_genre
            possible_audios = search_audio_using_attributes(prev_audio_genre, answered_audios_id)
            if not possible_audios:
                raise NoMatchingAudioError(f'No matching audios in question index {question_index + 1} and progress {test.progress}')
            next_audio = random.choice(possible_audios)

    if test_progress == "analyzing additional preference":
        prev_audio = AudioFile.query.get_or_404(prev_answer.audio_id)
        if prev_answer.rating >= 2:
            next_criteria = random.choice(["dominant_genre", "dominant_mood", "dominant_vocal"])
            prev_answer_attribute = getattr(prev_audio, next_criteria)
            possible_audios = search_audio_using_attributes(prev_answer_attribute, answered_audios_id)
            if not possible_audios:
                raise NoMatchingAudioError(f'No matching audios in question index {question_index + 1} and progress {test.progress}')
            next_audio = random.choice(possible_audios)
            
        else:
            disparate_audios = AudioFile.query.filter(
                    AudioFile.dominant_genre != prev_audio.dominant_genre,
                    AudioFile.dominant_mood != prev_audio.dominant_mood,
                    AudioFile.dominant_vocal != prev_audio.dominant_vocal,
                ).all()
            if not disparate_audios:
                    raise NoMatchingAudioError(f'No matching audios in question index {question_index + 1} and progress {test.progress}')
            disparate_audios = [audio for audio in disparate_audios if audio.id not in answered_audios_id]
            next_audio = random.choice(disparate_audios)
    
    test.progress = test_progress
    db.session.commit()
    return next_audio.id

def get_next_audio_for_test_type_2(test_id, question_index):
    #get existing answers data (including audio ids)
    test = Test.query.get(test_id)
    test_progress = test.progress
    print("question_index: ", question_index)
    #if there is an existing answer, go to the question
    existing_next_answer = UserAnswer.query.filter_by(test_id=test_id, user_id=current_user.id, question_index=question_index+1).first()
    if existing_next_answer:
        next_audio_id = existing_next_answer.audio_id
        return next_audio_id

    answers = UserAnswer.query.filter_by(test_id=test_id).all()   
    answered_audios_id = [answer.audio_id for answer in answers]
    prev_answer = UserAnswer.query.filter_by(test_id=test_id, user_id=current_user.id, question_index=question_index).first()

    #user's preferred genres in presurvey
    preferred_genres = test.decoded_pre_survey_answers['3']
    explorative_genre_columns = [genre for genre in genre_columns if genre not in preferred_genres]

    if test_progress == "searching genre preference":
        print("progress: searching genre preference")
        answered_audios = [AudioFile.query.get_or_404(audio_id) for audio_id in answered_audios_id]
        answered_genres = [answer.dominant_genre for answer in answered_audios]
        unanswered_genres = [genre for genre in explorative_genre_columns if genre not in answered_genres]
        if not unanswered_genres:
            test_progress = "analyzing genre preference"
        else:
            next_question_genre = random.choice(unanswered_genres)
            possible_audios = search_audio_using_attributes(next_question_genre, answered_audios_id)
            if not possible_audios:
                raise NoMatchingAudioError(f'No matching audios in question index {question_index + 1} and progress {test.progress}')
            next_audio = random.choice(possible_audios)
    
    if test_progress == "analyzing genre preference":
        print("progress: analyzing genre preference")
        if len(answers) == len(explorative_genre_columns):
            #algorithm getting the best rated genre
            genre_score = {genre:0 for genre in explorative_genre_columns}
            for answer in answers:
                audio_genre = AudioFile.query.get_or_404(answer.audio_id).genre
                for genre, value in audio_genre.items():
                    if genre in explorative_genre_columns:
                        genre_score[genre] += value
            preferred_genre = max(genre_score, key=genre_score.get)
            possible_audios = search_audio_using_attributes(preferred_genre, answered_audios_id)
            if not possible_audios:
                raise NoMatchingAudioError(f'No matching audios in question index {question_index + 1} and progress {test.progress}')
            next_audio = random.choice(possible_audios)  

        elif len(answers) >= len(explorative_genre_columns) + 7:
            test_progress = "analyzing additional preference"
        
        else:
            prev_audio_genre = AudioFile.query.get_or_404(prev_answer.audio_id).dominant_genre
            possible_audios = search_audio_using_attributes(prev_audio_genre, answered_audios_id)
            if not possible_audios:
                raise NoMatchingAudioError(f'No matching audios in question index {question_index + 1} and progress {test.progress}')
            next_audio = random.choice(possible_audios)
        
    if test_progress == "analyzing additional preference":
        print("progress: analyzing additional preference")
        prev_audio = AudioFile.query.get_or_404(prev_answer.audio_id)
        if prev_answer.rating >= 2:
            next_criteria = random.choice(["dominant_genre", "dominant_mood", "dominant_vocal"])
            prev_answer_attribute = getattr(prev_audio, next_criteria)
            possible_audios = search_audio_using_attributes(prev_answer_attribute, answered_audios_id)
            if not possible_audios:
                raise NoMatchingAudioError(f'No matching audios in question index {question_index + 1} and progress {test.progress}')
            next_audio = random.choice(possible_audios)
            
        else:
            disparate_audios = AudioFile.query.filter(
                    AudioFile.dominant_genre != prev_audio.dominant_genre,
                    AudioFile.dominant_mood != prev_audio.dominant_mood,
                    AudioFile.dominant_vocal != prev_audio.dominant_vocal,
                ).all()
            if not disparate_audios:
                    raise NoMatchingAudioError(f'No matching audios in question index {question_index + 1} and progress {test.progress}')
            
            disparate_audios = [audio for audio in disparate_audios if audio.id not in answered_audios_id]
            next_audio = random.choice(disparate_audios)
    
    answers = UserAnswer.query.filter_by(user_id=current_user.id, test_id=test.id).all()
    print("answers submitted: ", answers)
    
    test.progress = test_progress
    db.session.commit()
    return next_audio.id


def get_next_audio_for_test_type_3(test_id, question_index):
    #get existing answers data (including audio ids)
    test = Test.query.get(test_id)
    test_progress = test.progress
    print("question_index: ", question_index)    
    #if there is an existing answer, go to the question
    existing_next_answer = UserAnswer.query.filter_by(test_id=test_id, user_id=current_user.id, question_index=question_index+1).first()
    if existing_next_answer:
        next_audio_id = existing_next_answer.audio_id
        return next_audio_id

    answers = UserAnswer.query.filter_by(test_id=test_id).all()   
    answered_audios_id = [answer.audio_id for answer in answers]

    #get current question index
    prev_answer = UserAnswer.query.filter_by(test_id=test_id) \
                                  .order_by(UserAnswer.question_index.desc()).first()

    #user's preferred genres in presurvey
    preferred_genres = test.decoded_pre_survey_answers['3']
    
    #search audios of corresponding genres 
    possible_audios = search_audio_using_attributes(preferred_genres[0], answered_audios_id)
    possible_audios += (search_audio_using_attributes(preferred_genres[1], answered_audios_id) if len(preferred_genres) == 2 else [])

    if not possible_audios:
        raise NoMatchingAudioError(f'No matching audios in question index {question_index + 1} and progress {test.progress}')
    
    next_audio = random.choice(possible_audios)

    return next_audio.id