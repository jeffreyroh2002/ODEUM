from flask import Blueprint, jsonify, request, session, redirect, url_for
from api import db, bcrypt
from api.models import User, AudioFile, UserAnswer, Test
#from api.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_wtf.csrf import generate_csrf
from flask_login import login_user, current_user, logout_user, login_required
import re  # for email confirmation
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return("Welcome to Flask App!")

@main.route('/csrf-token')
def csrf_token():
    return jsonify({'csrf_token': generate_csrf()})

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
    data = request.json

    # Validate input fields (instead of form.validate_on_submit())
    if 'first_name' not in data or 'email' not in data or 'password' not in data or 'confirm_password' not in data:
        return jsonify({"error": "Missing required field(s)"}), 400

    first_name = data['first_name']
    email = data['email']
    password = data['password']
    confirm_password = data['confirm_password']

     # Additional validation
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return jsonify({"error": "Invalid email format"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400
    
    if password != confirm_password:
        return jsonify({"error": "Password and Confirm Password do not match"}), 400

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
def login():
    data = request.json

    # Validate input fields (instead of form.validate_on_submit())
    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing required field(s)"}), 400

    email = request.json["email"]
    password = request.json["password"]
    remember_me = request.json["remember_me"]

    user = User.query.filter_by(email=email).first()

    if user is None or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Check email or password"}), 401
    
    login_user(user, remember=remember_me)
    session["user_id"] = user.id
    
    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "email": user.email
    })

@main.route('/logout', methods=["POST"])
@login_required  # Require the user to be logged in to access this route
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"})

@main.route('/isLoggedIn')
def is_logged_in():
    if current_user.is_authenticated:
        return jsonify({"isLoggedIn": True})
    else:
        return jsonify({"isLoggedIn": False})

def get_next_audio_file_id(current_audio_file_id):
    current_audio_file = AudioFile.query.get_or_404(current_audio_file_id)
    next_audio_file = AudioFile.query.filter(AudioFile.id > current_audio_file.id).order_by(AudioFile.id.asc()).first()

    if next_audio_file:
        return next_audio_file.id
    else:
        return None

@main.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    data = request.json
    new_answer = UserAnswer(
        overall_rating=data['overall_rating'],
        genre_rating=data['genre_rating'],
        mood_rating=data['mood_rating'],
        vocal_timbre_rating=data['vocal_timbre_rating'],
        user_id=current_user.id,  # Assuming you're using Flask-Login for user management
        audio_id=data['audio_id'],
        test_id=data['test_id'],
    )
    db.session.add(new_answer)
    db.session.commit()

    next_audio_file_id = get_next_audio_file_id(data['audio_id'])

    if next_audio_file_id is not None:
        return jsonify({'message': 'Answer submitted successfully', 'next_audio_file_id': next_audio_file_id})
    else:
        # Handle the case where there are no more audio files
        user = current_user
        test = Test.query.filter((Test.user_id==user.id) & (Test.test_type==test_type)).order_by(Test.test_start_time.desc()).first()
        test.test_end_time = datetime.now()
        db.session.commit()
        return jsonify({'message': 'Test completed', 'next_audio_file_id': None})

@login_required
@main.route('/get_next_questions', methods=["GET","POST"])
def get_next_questions():
    test_type = request.args.get('test_type')
    audio_file_id = request.args.get('audio_file_id')

    user = current_user

    # consider case where user already took test: new test
    test = Test.query.filter((Test.user_id==user.id) & (Test.test_type==test_type)).order_by(Test.test_start_time.desc()).first()

    if audio_file_id == 0:
        # haven't taken this test before (new user)
        if not test:
            # add new test data to Test model
            test_val = Test(
                test_type = test_type,
                test_start_time = datetime.now(),
                subject = user
            )
            db.session.add(test_val)
            db.session.commit()

            return redirect(url_for('main.get_next_questions', test_type=test_type, audio_file_id=1))

        # already have taken this test before (start new test)
        if test.test_end_time:
            # add new test data to Test model
            test_val = Test(
                test_type = test_type,
                test_start_time = datetime.now(),
                subject = user
            )
            db.session.add(test_val)
            db.session.commit()

            ### change below flash to display on react frontend ###
            # flash('You have already taken this type of test before. Start test again.', 'info')
            
            return redirect(url_for('main.get_next_questions', test_type=test_type, audio_file_id=1))

        latest_answer = UserAnswer.query.filter((UserAnswer.user==current_user) & (UserAnswer.test==test)).order_by(UserAnswer.audio_id.desc()).first()
        if not latest_answer :
            return redirect(url_for('main.get_next_questions', test_type=test_type, audio_file_id=1))
        latest_audio_num = latest_answer.audio_id

        # when you have already finished this type of test
        if len(AudioFile.query.all()) == latest_audio_num:
            ### change below flash message and redirect to results page in react frontend ###
            # flash('You have already taken this test!', 'info')
            # return redirect(url_for('results.single_test_result', test_id=test.id))
            print('You have already taken this test! Taking you to test results...')
        else:
            ### change below flash message ###
            # flash('It seems you have already answers some questions in the past. Starting where you left off.', 'info')
            return redirect(url_for('main.get_next_questions', test_type=test_type, audio_file_id=latest_audio_num+1))

    audio_file = AudioFile.query.get_or_404(audio_file_id)
    return jsonify(audio_file) # sending to react frontend



@login_required
@main.route('/get_prev_questions', methods=["GET"])
def get_prev_questions(test_type, audio_file_id):
    """ NEED TO RECREATE THIS ENTIRELY
    db_answer = UserAnswer.query.filter((UserAnswer.test == test) & (UserAnswer.audio == audio_file) & (UserAnswer.user == current_user)).first()
    form.overall_rating.default = db_answer.overall_rating
        form.genre_rating.default = db_answer.genre_rating
        form.mood_rating.default = db_answer.mood_rating
        form.vocal_timbre_rating.default = db_answer.vocal_timbre_rating
        if db_answer.genre_not_sure:
            form.genre_not_sure.default = True
        if db_answer.mood_not_sure:
            form.mood_not_sure.default = True
        if db_answer.vocal_not_sure:
            form.vocal_not_sure.default = True
        form.process()
    """