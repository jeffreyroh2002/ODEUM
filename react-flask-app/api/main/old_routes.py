from flask import Blueprint, jsonify, request, session, redirect, url_for
from api import db, bcrypt
from api.models import User, AudioFile, UserAnswer, Test
#from api.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_wtf.csrf import generate_csrf
from flask_login import login_user, current_user, logout_user, login_required
import re  # for email confirmation
from datetime import datetime
import logging
import json

from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict
import statistics
import matplotlib.pyplot as plt

#imports for saving png files
import io
import base64
import matplotlib.pyplot as plt
from flask import render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator
from collections import defaultdict
import seaborn as sns


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
    print("HELLOW WORLD!!!!")
    logout_user()
    return jsonify({"message": "Logout successful"})

@main.route('/isLoggedIn')
def is_logged_in():
    if current_user.is_authenticated:
        return jsonify({"isLoggedIn": True})
    else:
        return jsonify({"isLoggedIn": False})

def get_next_audio_file_id(current_audio_file_id):
    # Query for the next AudioFile ID greater than the current one
    next_audio_file = AudioFile.query.filter(AudioFile.id > current_audio_file_id).order_by(AudioFile.id).first()
    return next_audio_file.id if next_audio_file else None

def get_prev_audio_file_id(current_audio_file_id):
    # Query for the previous AudioFile ID less than the current one
    prev_audio_file = AudioFile.query.filter(AudioFile.id < current_audio_file_id).order_by(AudioFile.id.desc()).first()
    return prev_audio_file.id if prev_audio_file else None

@main.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    data = request.json
    print("submit answer test id submited:", data['test_id'])
    new_answer = UserAnswer(
        overall_rating=data['overall_rating'],
        genre_rating=data['genre_rating'],
        mood_rating=data['mood_rating'],
        vocal_timbre_rating=data['vocal_timbre_rating'],
        user_id=current_user.id,
        audio_id=data['audio_id'],
        test_id=data['test_id'],
    )
    
    db.session.add(new_answer)
    db.session.commit()

    next_audio_file_id = get_next_audio_file_id(data['audio_id'])
    test = Test.query.filter_by(user_id=current_user.id, id=data['test_id']).first()
    
    if next_audio_file_id is not None:
        #add logic to call the next values if available
        next_audio_file = AudioFile.query.get(next_audio_file_id)
        db_answer = UserAnswer.query.filter((UserAnswer.test == test) & (UserAnswer.audio_id == next_audio_file.id) & (UserAnswer.user == current_user)).first()
        print("next db_answer:", db_answer)
        if db_answer == None:
            return jsonify({
                'message': 'Answer submitted successfully', 
                'next_audio_file_id': next_audio_file_id, 
                'test_id': test.id,
                'overall_rating': None,
                'genre_rating': 0,
                'mood_rating': 0,
                'vocal_timbre_rating': 0
            })
        else:
            return jsonify({
                'message': 'Answer submitted successfully', 
                'next_audio_file_id': next_audio_file_id, 
                'test_id': test.id,
                'overall_rating': db_answer.overall_rating,
                'genre_rating': db_answer.genre_rating,
                'mood_rating': db_answer.mood_rating,
                'vocal_timbre_rating': db_answer.vocal_timbre_rating
            })
    else:
        # Handle the case where there are no more audio files
        user = current_user
        print("TEST TEST TEST!:", test )
        test.test_end_time = datetime.now()
        db.session.commit()
        print("TEST TEST TEST!:", test )
        return jsonify({'message': 'Test completed', 'next_audio_file_id': None, 'test_id': test.id})
    

@main.route('/before_test_info', methods=['GET'])
@login_required
def before_test_info():

    user = current_user
    #test = Test.query.filter_by(user_id=user.id, test_type=1).order_by(Test.test_start_time.desc()).first()
    test = Test.query.filter_by(user_id=user.id, test_type=1).order_by(Test.test_start_time.desc()).first()
    print(test)
    # haven't taken this test before or need to start a new one
    if not test or test.test_end_time:
        print("CREATING NEW TEST NOW!")
        test_val = Test(
            test_type = 1,
            test_start_time = datetime.now(),
            subject = user
        )
        db.session.add(test_val)
        db.session.commit()
        audio_file_id = 1
        audio_file = AudioFile.query.get_or_404(audio_file_id)

        newTest = True
        test = Test.query.filter_by(user_id=user.id, test_type=1).order_by(Test.test_start_time.desc()).first()
        print("new test id:", test.id)
        print("IM ABOUT TO GO BACK TO FRONTEND")
        print("audio_file", audio_file)
        return jsonify({
                    'status': 'in_progress',
                    'new_test': newTest,
                    'audio_file_id': audio_file_id,
                    'audio_file_name': audio_file.audio_name,
                    'test_id': test.id
        })
    

    #need to continue ongoing test
    else:
        print("BEFORE LAST answer:")
        newTest = False
        last_answer = UserAnswer.query.order_by(UserAnswer.id.desc()).first()
        if last_answer == None:
            audio_file = AudioFile.query.get_or_404(1)
            return jsonify({
                    'status': 'in_progress',
                    'new_test': newTest,
                    'audio_file_id': audio_file.id,
                    'audio_file_name': audio_file.audio_name,
                    'test_id': test.id
        })
        else:
            print("last answer:", last_answer)
            audio_file_id = last_answer.audio_id
            print("audio_file_id:", audio_file_id)
            audio_file = AudioFile.query.get_or_404(audio_file_id)
            print("audio_file:", audio_file)
            newTest = False
            # print("new audio file id: ",audio_file_id)
            return jsonify({
                        'status': 'in_progress',
                        'new_test': newTest,
                        'audio_file_id': audio_file_id,
                        'audio_file_name': audio_file.audio_name,
                        'test_id': test.id
            })

@login_required
@main.route('/get_next_questions', methods=["GET"])
def get_next_questions():

    test_type = request.args.get('test_type', type=int)
    audio_file_id = request.args.get('audio_file_id', type=int)
    test_id = request.args.get('test_id', type=int)
    print("TESTID!!!!:", test_id)

    if not test_type or audio_file_id is None:
        return jsonify({'error': 'Missing required parameters'}), 400

    user = current_user

    # Find the latest test of the specified type for the user
    test = Test.query.filter_by(user_id=user.id, test_type=test_type, id=test_id).order_by(Test.test_start_time.desc()).first()
    print("current test!:", test)
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
@main.route('/get_prev_questions', methods=["POST"])
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
    print("HERE IS TEST!:", test)

    # Continue with the ongoing test
    print("audio_id:",audio_id)

    prev_audio_file_id = get_prev_audio_file_id(audio_id)
    print("prev_audio_id:", prev_audio_file_id)
    if prev_audio_file_id != None:
        prev_audio_file = AudioFile.query.get(prev_audio_file_id)
        print("prev_audio_file:", prev_audio_file)
        db_answer = UserAnswer.query.filter((UserAnswer.test == test) & (UserAnswer.audio_id == prev_audio_file.id) & (UserAnswer.user == current_user)).first()
        print("db_answer:", db_answer)
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

@login_required
@main.route('/get_user_info', methods=["GET"])
def get_user_info():
    user = current_user
    user_name = user.first_name
    tests = Test.query.filter_by(subject=current_user).order_by(Test.id.asc()).all()
    tests_data = []
    
    for test in tests:
        test_data = {
            'id': test.id,
            'test_type': test.test_type,
            'test_start_time': test.test_start_time.strftime('%Y-%m-%d %H:%M:%S'),  # Convert datetime to string
        }
        if (test.test_end_time):
            tests_data.append(test_data)

    return jsonify({
        'user_name': user_name,
        'tests_data': tests_data
    })


def get_attribute_name(index):
    # Define the order of attributes in your feature vectors
    attributes = ['Rock','Hip Hop','Pop Ballad','Electronic','Korean Ballad','Jazz','R&B/Soul', 
                  'Tense', 'Bright', 'Emotional', 'Relaxed', 
                  'Smooth', 'Dreamy', 'Raspy', 'Voiceless']
    
    # Return the attribute name corresponding to the given index
    return attributes[index]

@main.route("/test_results", methods=['GET'])
@login_required
def test_results():
    test_id = request.args.get('testId')

    #calculate all characteristics
    user = current_user
    print(user)
    test = Test.query.filter_by(id=test_id).first()
    print(test)
    if test.subject != current_user: 
        return jsonify({'error': 'User does not match test owner'}), 403

    display_messages = []
    
    #Update Preference each Song
    genre_score = {'Rock': 0,'Hip Hop': 0,'Pop Ballad': 0,'Electronic': 0,'Korean Ballad': 0,'Jazz': 0,'R&B/Soul': 0}
    mood_score = {'Tense': 0, 'Bright': 0, 'Emotional': 0, 'Relaxed': 0}
    vocal_score = {'Smooth': 0,'Dreamy': 0,'Raspy': 0,'Voiceless': 0}

    # High Rating song tracker
    high_rated_songs = []

    test_answer = UserAnswer.query.filter_by(user=user).all()
    print("test_answer", test_answer)

    answers = UserAnswer.query.filter_by(test_id=test_id).all()
    print ("answers:", answers)
    for answer in answers:
        audio = AudioFile.query.get(answer.audio_id)

        #from audioFile model
        genre_pred = audio.genre   #assuming audioFile is populated with scores using dictionaries with same keys
        mood_pred = audio.mood
        vocal_pred = audio.vocal

        print("genre prediciton input:", genre_pred)
        print("mood prediciton input:", mood_pred)

        #from Questions Form
        overall_rating = answer.overall_rating   # need to use this
        genre_rating = answer.genre_rating
        mood_rating = answer.mood_rating
        vocal_rating = answer.vocal_timbre_rating

        #Calculate overall score
        #Calculate each genre score
        genre_weighted = {}
        if genre_pred and not isinstance(audio.genre, float):
            genre_scores = audio.genre
            try:
                genre_data = json.loads(genre_scores)
            except json.JSONDecodeError:
                print("Error decoding genre_data JSON.")
                return jsonify({'error: Error decoding genre_data JSON'}), 404 

            #if user is not sure about the genre, calculate the genre_score based on overall rating
            if genre_rating == 0:
                for genre_name, proportion in genre_data.items():
                    genre_weighted[genre_name] = proportion * overall_rating
            
            #in other case, calculate the genre_score based on (0.3 portion of overall_rating) and (0.7 portion of genre_rating)
            else:
                for genre_name, proportion in genre_data.items():
                    genre_weighted[genre_name] = (proportion * overall_rating * 0.3) + (proportion * genre_rating * 0.7)

            for genre in genre_weighted:
                genre_score[genre] += genre_weighted[genre]

        else:
            print("Genre data is not available or is in an unexpected format.")
            return jsonify({'error: Genre data is not available or is in an unexpected format'}), 404 

        #Calculate each mood score
        mood_weighted = {}
        if mood_pred and not isinstance(audio.mood, float):
            mood_scores = audio.mood
            try:
                mood_data = json.loads(mood_scores)
            except json.JSONDecodeError:
                print("Error decoding mood_data JSON.")
                return jsonify({'error: Error decoding mood_data JSON'}), 404 

            #if user is not sure about the mood, calculate the mood_score based on overall rating
            if mood_rating == 0:
                for mood_name, proportion in mood_data.items():
                    mood_weighted[mood_name] = proportion * overall_rating
            
            #in other case, calculate the mood_score based on (0.3 portion of overall_rating) and (0.7 portion of mood_rating)
            else:
                for mood_name, proportion in mood_data.items():
                    mood_weighted[mood_name] = (proportion * overall_rating * 0.3) + (proportion * mood_rating * 0.7)

            for mood in mood_weighted:
                mood_score[mood] += mood_weighted[mood]

        else:
            print("Mood data is not available or is in an unexpected format.")
            return jsonify({'error: Mood data is not available or is in an unexpected format'}), 404 

        #Calculate each vocal timbre score
        vocal_weighted = {}
        if vocal_pred and not isinstance(audio.vocal, float):
            vocal_scores = audio.vocal
            try:
                vocal_data = json.loads(vocal_scores)
            except json.JSONDecodeError:
                print("Error decoding vocal_data JSON.")
                return jsonify({'error: Error decoding vocal_data JSON'}), 404 

            #if user is not sure about the vocal, calculate the vocal_score based on overall rating
            if vocal_rating == 0:
                for vocal_name, proportion in vocal_data.items():
                    vocal_weighted[vocal_name] = proportion * overall_rating
            
            #in other case, calculate the vocal_score based on (0.3 portion of overall_rating) and (0.7 portion of vocal_rating)
            else:
                for vocal_name, proportion in vocal_data.items():
                    vocal_weighted[vocal_name] = (proportion * overall_rating * 0.3) + (proportion * vocal_rating * 0.7)

            for vocal in vocal_weighted:
                vocal_score[vocal] += vocal_weighted[vocal]

        else:
            print("Vocal data is not available or is in an unexpected format.")
            return jsonify({'error: Vocal data is not available or is in an unexpected format'}), 404 
        
    # store highly rated songs into high_rated songs list
        if (overall_rating >= 2):
            high_rated_songs.append(answer.audio_id)

    # array of arrays to store each feature vector of highly rated songs
    high_rated_feature_vectors = []
    for high_rated_song in high_rated_songs:
        audio = AudioFile.query.get(high_rated_song)
        genre_data = json.loads(audio.genre)
        mood_data = json.loads(audio.mood)
        vocal_data = json.loads(audio.vocal)

        # Flatten the dictionaries into a single array
        feature_vector = list(genre_data.values()) + list(mood_data.values()) + list(vocal_data.values())

        # Normalize the feature vector
        normalized_vector = normalize([feature_vector])[0]
        high_rated_feature_vectors.append(normalized_vector)

    
    ## ALGORITHM FOR CUSTOM BINNING HISTORGRAM ##

    # Initialize a dictionary to store all values for each attribute
    attribute_values = defaultdict(list)

    # Collect values for each attribute across all high-rated songs
    for vector in high_rated_feature_vectors:
        for attr_index, value in enumerate(vector):
            attribute_name = get_attribute_name(attr_index)
            attribute_values[attribute_name].append(value)

    # Determine the most populated range for each attribute
    attribute_ranges = {}
    range_size = 0.2  # Define the size of each range

    for attr, values in attribute_values.items():
        # Filter out values less than or equal to 0.2
        filtered_values = [value for value in values if value > 0.2]

        # Bin values into ranges starting from 0.2
        bins = np.arange(0.2, 1 + range_size, range_size)
        hist, bin_edges = np.histogram(filtered_values, bins=bins)

        # Find the range with the maximum count
        max_count_index = np.argmax(hist)
        common_range = (bin_edges[max_count_index], bin_edges[max_count_index + 1])
        
        attribute_ranges[attr] = common_range


    # Prepare the display message
    display_messages.append("Most common ranges for attributes in your top-rated songs (excluding 0 to 0.2):")
    for attr, common_range in attribute_ranges.items():
        display_messages.append(f"- {attr}: Most Common Range {common_range}")


    # PLOTTING DENSITY PLOT

    # Initialize a dictionary to store all values for each attribute
    attribute_values = defaultdict(list)

    # Collect values for each attribute across all high-rated songs
    for vector in high_rated_feature_vectors:
        for attr_index, value in enumerate(vector):
            attribute_name = get_attribute_name(attr_index)
            if value > 0.2:  # Exclude values between 0.0 and 0.2
                attribute_values[attribute_name].append(value)

    # Define color palettes for each category
    genre_colors = sns.color_palette('Set1', len(genre_score))
    mood_colors = sns.color_palette('Set2', len(mood_score))
    vocal_colors = sns.color_palette('Set3', len(vocal_score))

    
    # Create a combined density plot for each category

    # Plot for Genres
    plt.figure(figsize=(5, 3))
    for (genre, _), color in zip(genre_score.items(), genre_colors):
        sns.kdeplot(attribute_values[genre], label=genre, color=color, fill=True, bw_adjust=0.5)
    plt.title('Density Plots for Genres', fontsize=14)
    plt.xlabel('Attribute Values', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend()
    plt.tight_layout()
    # Save the first plot
    genre_png = io.BytesIO()
    plt.savefig(genre_png, format='png')
    genre_png.seek(0)
    genre_encoded = base64.b64encode(genre_png.getvalue()).decode('utf-8')
    plt.close()

    # Plot for Moods
    plt.figure(figsize=(5, 3))
    for (mood, _), color in zip(mood_score.items(), mood_colors):
        sns.kdeplot(attribute_values[mood], label=mood, color=color, fill=True, bw_adjust=0.5)
    plt.title('Density Plots for Moods', fontsize=14)
    plt.xlabel('Attribute Values', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend()
    plt.tight_layout()
    # Save the second plot
    mood_png = io.BytesIO()
    plt.savefig(mood_png, format='png')
    mood_png.seek(0)
    mood_encoded = base64.b64encode(mood_png.getvalue()).decode('utf-8')
    plt.close()

    # Plot for Vocals
    plt.figure(figsize=(5, 3))
    for (vocal, _), color in zip(vocal_score.items(), vocal_colors):
        sns.kdeplot(attribute_values[vocal], label=vocal, color=color, fill=True, bw_adjust=0.5)
    plt.title('Density Plots for Vocals', fontsize=14)
    plt.xlabel('Attribute Values', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend()
    plt.tight_layout()
    # Save the third plot
    vocal_png = io.BytesIO()
    plt.savefig(vocal_png, format='png')
    vocal_png.seek(0)
    vocal_encoded = base64.b64encode(vocal_png.getvalue()).decode('utf-8')
    plt.close()

    print("user.id:", user.id)
    print("test.id:", test.id)
    print("test_type:", test.test_type)
    print("genre_score:", genre_score)
    print("mood_score:", mood_score)
    print("vocal_score:", vocal_score)
    """
    print("genre_encoded:", genre_encoded)
    print("mood_encoded:", mood_encoded)
    print("vocal_encoded:", vocal_encoded)
    """
    print("display_messages:", display_messages)

    # Pass the encoded images and other necessary information to the template
    response_data = {
        'user_id': user.id,
        'test_id': test.id,
        'test_type': test.test_type,
        'genre_score': genre_score,
        'mood_score': mood_score,
        'vocal_score': vocal_score,
        'genre_image': genre_encoded,
        'mood_image': mood_encoded,
        'vocal_image': vocal_encoded,
        'display_messages': display_messages
    }
    return jsonify(response_data)
