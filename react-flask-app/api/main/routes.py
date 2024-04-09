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
import pandas as pd
from sklearn.decomposition import PCA
pd.set_option('display.max_columns', None)

from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import numpy as np
from collections import defaultdict
import statistics
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from mlxtend.frequent_patterns import apriori, association_rules



#imports for saving png files
import io
import base64
from flask import render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator
from collections import defaultdict
import seaborn as sns
import os

#openAI, langchain modules
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage



main = Blueprint('main', __name__)

NUM_AUDIO = 22
NUM_QUESTIONS_PER_AUDIO = 4
EXTRA_QUESTIONS = 0
EXTRA_QUESTIONS_INDEX = []
TOTAL_QUESTIONS = NUM_AUDIO * NUM_QUESTIONS_PER_AUDIO + EXTRA_QUESTIONS

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

@main.route('/is_logged_in')
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

@login_required
@main.route('/get_useranswer', methods=['GET'])
def get_useranswer():
    audio_id = int(request.args.get('audio_id'))
    test_id = int(request.args.get('test_id'))
    question_type = request.args.get('question_type')
    print(audio_id, test_id, question_type)
    answer = UserAnswer.query.filter_by(test_id=test_id, audio_id=audio_id).first()
    if answer == None:
        rating = None
    else:
        rating = getattr(answer, question_type)
    print("saved rating: ", rating)
    return jsonify({"rating" : rating})

@main.route('/get_question_metadata', methods=['GET'])
@login_required
def get_question_metadata():
    question_index = request.args.get('question_index', type=int)
    question_types = ['vocal_timbre_rating', 'overall_rating', 'genre_rating', 'mood_rating']
    
    if question_index in EXTRA_QUESTIONS_INDEX:
        question_type = 'additional'
    
    else:
        additional_q_before = [index for index in EXTRA_QUESTIONS_INDEX if index < question_index]
        num_additional_q_before = len(additional_q_before)
        question_index_except_additional = question_index - num_additional_q_before      
        question_type = question_types[question_index % NUM_QUESTIONS_PER_AUDIO]
        audio_id = (question_index_except_additional - 1) // NUM_QUESTIONS_PER_AUDIO + 1

        dir_path = "/workspace/ODEUM/react-flask-app/api/static/audio_files"
        filenames = os.listdir(dir_path)
        full_filenames = ['static/audio_files/' + filename for filename in filenames]
        print("askjaskf: ", question_type, audio_id, full_filenames[int(audio_id) - 1])
    return jsonify({"question_type" : question_type, "audio_id" : audio_id,
                    "audio_filename": full_filenames[int(audio_id) - 1]})

@main.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    question_index = int(data['question_index'])
    answer_type = data['type']
    audio_index = int(data['audio_id'])
    rating = data['rating']
    test_id = int(data['test_id'])
    print("get data: ", question_index, answer_type, audio_index, rating, test_id)
    answer = UserAnswer.query.filter_by(test_id=test_id, audio_id=audio_index).first()
    if answer_type == 'overall_rating' and not answer:
        print("new answer added")
        new_answer = UserAnswer(audio_id=audio_index, test_id=test_id, user_id=current_user.id)
        db.session.add(new_answer)
        db.session.commit()
        answer = UserAnswer.query.filter_by(audio_id=audio_index, test_id=test_id, user_id=current_user.id).first()

    setattr(answer, answer_type, rating)
    db.session.commit()
    answer = UserAnswer.query.filter_by(test_id=test_id, audio_id=audio_index).first()

    print(answer.overall_rating, answer.genre_rating, answer.mood_rating, answer.vocal_timbre_rating)

    if question_index == TOTAL_QUESTIONS:
        test = Test.query.get(test_id)
        test.test_end_time = datetime.now()
        db.session.commit()
        
    return jsonify({"Hello": "World"})
    
@main.route('/before_test_info', methods=['GET'])
@login_required
def before_test_info():
    user = current_user
    num_audio = 22
    test = Test.query.filter_by(user_id=user.id, test_type=1).order_by(Test.test_start_time.desc()).first()

    if not test or test.test_end_time:        
        test_val = Test(
            test_type = 1,
            test_start_time = datetime.now(),
            subject = user
        )
        db.session.add(test_val)
        db.session.commit()
        is_new_test = True
        question_index = 1
        test = Test.query.filter_by(user_id=user.id, test_type=1).order_by(Test.test_start_time.desc()).first()

    else:
        is_new_test = False
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
                'new_test': is_new_test,
                'question_index': question_index,
                'test_id': test.id
    })


@login_required
@main.route('/get_next_questions', methods=["GET"])
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
@main.route('/get_audio_num', methods=["GET"])
def get_audio_num():
    dir_path = "/workspace/ODEUM/react-flask-app/api/static/audio_files"
    filenames = os.listdir(dir_path)
    return jsonify({"num_audio": len(filenames)})

@login_required
@main.route('/get_audio_filename', methods=["GET"])
def get_audio_filename():
    audio_id = request.args.get('audio_id')
    dir_path = "/workspace/ODEUM/react-flask-app/api/static/audio_files"
    filenames = os.listdir(dir_path)
    full_filenames = ['static/audio_files/' + filename for filename in filenames]
    return jsonify({"audio_filename": full_filenames[int(audio_id) - 1]})


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

def prepare_structured_data(test_answers):
    """Extracts and structures data from test answers."""
    structured_data = []
    for answer in test_answers:
        audio = AudioFile.query.filter_by(id=answer.audio_id).first()
        if audio:
            data_row = {
                "overall_rating": answer.overall_rating,
                "genre_rating": answer.genre_rating,
                "mood_rating": answer.mood_rating,
                "vocal_timbre_rating": answer.vocal_timbre_rating,
                **audio.genre,
                **audio.mood,
                **audio.vocal
            }
            structured_data.append(data_row)
    return structured_data

def create_user_ratings_df(test_answers):
    """Creates a DataFrame from test answers containing user ratings."""
    user_ratings = pd.DataFrame([
        {'user_id': answer.user_id, 'song_id': answer.audio_id, 'rating': answer.overall_rating}
        for answer in test_answers
    ])
    return user_ratings

def perform_kmeans_clustering(df, feature_columns, n_clusters=5):
    """Performs KMeans clustering on the given DataFrame."""
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[feature_columns])
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    df['cluster'] = kmeans.fit_predict(scaled_features)
    return df, kmeans

# FOR PRINT STATEMENT (CHECKING)
def analyze_cluster_ratings(user_ratings_clustered, n_clusters):
    #Analyzes and prints average ratings by cluster, including which clusters are generally liked or disliked.
    avg_ratings_by_cluster = user_ratings_clustered.groupby(['user_id', 'cluster'])['rating'].mean().reset_index()

    print("\nAverage Ratings by Cluster:")
    print(avg_ratings_by_cluster.head())

    # Analyze which clusters are rated more positively on average
    for cluster_num in range(n_clusters):
        cluster_avg_rating = avg_ratings_by_cluster[avg_ratings_by_cluster['cluster'] == cluster_num]['rating'].mean()
        print(f"Cluster {cluster_num} Average Rating: {cluster_avg_rating}")

    # Further analysis can be done based on the findings
    liked_clusters = avg_ratings_by_cluster[avg_ratings_by_cluster['rating'] > 0].groupby('cluster')['rating'].mean()
    disliked_clusters = avg_ratings_by_cluster[avg_ratings_by_cluster['rating'] < 0].groupby('cluster')['rating'].mean()
    
    """
    print("\nLiked Clusters (Positive Average Rating):")
    print(liked_clusters)
    
    print("\nDisliked Clusters (Negative Average Rating):")
    print(disliked_clusters)
    """

def analyze_cluster_characteristics(df_clustered, n_clusters):
    """Analyzes the characteristics of each cluster."""
    cluster_characteristics = {}
    
    for cluster_label in range(n_clusters):
        cluster_data = df_clustered[df_clustered['cluster'] == cluster_label]
        cluster_centroid = cluster_data.mean()
        cluster_characteristics[cluster_label] = cluster_centroid
    
    return cluster_characteristics

"""
def analyze_cluster_ratings(user_ratings_clustered, n_clusters, feature_columns, save_plot=True):
    ###Analyzes and prints average ratings by cluster, including which clusters are generally liked or disliked.
    ###Also includes feature analysis, visualization, and interpretation of the clusters.
    # Step 1: Feature Analysis
    cluster_means = user_ratings_clustered.groupby('cluster')[feature_columns].mean()
    print("\nCluster Feature Means:")
    print(cluster_means)

    # Step 2: Visualization
    pca = PCA(n_components=2)
    cluster_centers_2D = pca.fit_transform(cluster_means)

    plt.figure(figsize=(10, 6))
    plt.scatter(cluster_centers_2D[:, 0], cluster_centers_2D[:, 1], c='red', marker='o', s=100)
    for i, txt in enumerate(cluster_means.index):
        plt.annotate(txt, (cluster_centers_2D[i, 0], cluster_centers_2D[i, 1]))
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title('Cluster Centers in 2D PCA Space')
    plt.grid(True)

    # Save plot as an image file
    if save_plot:
        plot_filename = 'cluster_centers_plot.png'
        plt.savefig(plot_filename)
        print(f"Plot saved as {plot_filename} in the current directory.")

    plt.show()

    # Step 3: Cluster Profiles
    cluster_profiles = cluster_means.transpose()
    print("\nCluster Profiles:")
    print(cluster_profiles)

    # Step 4: Interpretation
    print("\nInterpretation of Clusters:")
    for cluster_num in range(n_clusters):
        # Analyze which clusters are rated more positively on average
        cluster_avg_rating = user_ratings_clustered[user_ratings_clustered['cluster'] == cluster_num]['rating'].mean()
        print(f"\nCluster {cluster_num}:")
        print(f"Average Rating: {cluster_avg_rating}")
        if cluster_avg_rating > 0:
            print("This cluster is generally liked.")
        elif cluster_avg_rating < 0:
            print("This cluster is generally disliked.")
        else:
            print("This cluster has neutral sentiment.")
    
    # Further analysis can be done based on the findings
    liked_clusters = user_ratings_clustered[user_ratings_clustered['rating'] > 0].groupby('cluster')['rating'].mean()
    disliked_clusters = user_ratings_clustered[user_ratings_clustered['rating'] < 0].groupby('cluster')['rating'].mean()
    
    print("\nLiked Clusters (Positive Average Rating):")
    print(liked_clusters)
    
    print("\nDisliked Clusters (Negative Average Rating):")
    print(disliked_clusters)
"""

def find_significant_correlations(correlation_matrix, threshold, columns):
    significant_pairs = []
    for column in columns:
        for index, value in correlation_matrix[column].items():
            if abs(value) >= threshold and value != 1.0 and index != column:
                # Avoid self-correlation and ensure correlation meets threshold
                significant_pairs.append({"Attribute 1": column, "Attribute 2": index, "Correlation": value})

    significant_correlations = pd.DataFrame(significant_pairs)
    return significant_correlations

def calculate_significant_correlations_for_ratings(df, rating_columns, genre_columns, mood_columns, vocal_columns, threshold=0.7):
    """Calculates and prints significant correlations for each rating type with relevant song attributes,
    ensuring there's sufficient variability in attributes for meaningful analysis."""
    correlation_matrix = df.corr()
    
    # Exclude rating columns to focus on song attributes
    non_rating_columns = [col for col in df.columns if col not in rating_columns]
    
    # Ensure there's sufficient variability in attributes for meaningful analysis
    if len(non_rating_columns) <= len(rating_columns):
        print("Not enough variability in attributes for meaningful correlation analysis.")
        return
    
    # Mapping of rating types to their relevant attributes
    rating_to_attributes = {
        'overall_rating': genre_columns + mood_columns + vocal_columns,
        'genre_rating': genre_columns,
        'mood_rating': mood_columns,
        'vocal_timbre_rating': vocal_columns
    }

    for score in rating_columns:  # Iterate through each specific rating type
        relevant_attributes = rating_to_attributes.get(score, [])

        # Ensure attributes related to the score are in the correlation matrix
        valid_attributes = [attr for attr in relevant_attributes if attr in correlation_matrix.columns]

        for attribute in valid_attributes:
            # Calculate and print significant correlations for the attribute
            significant_correlations = find_significant_correlations(correlation_matrix, threshold, columns=[score, attribute])

            """
            if not significant_correlations.empty:
                print(f"\nSignificant Correlations for {score} with {attribute} (|correlation| >= {threshold}):\n", significant_correlations)
            else:
                print(f"\nNo significant correlations found for {score} with {attribute} at the threshold of {threshold}.")
            """

def perform_regression_analysis(df, genre_columns, mood_columns):
    """Performs regression analysis to model the impact of genre and mood on overall rating."""

    """
    # Print all columns
    print("Columns in DataFrame:")
    print(df.columns)
    
    # Print all rows
    print("Rows in DataFrame:")
    print(df)
    """

    # Check for NaN values in the DataFrame
    nan_indices = df[df.isna().any(axis=1)]
    if not nan_indices.empty:
        print("Rows with NaN values:")
        print(nan_indices)
        print("Please handle missing values appropriately before proceeding with regression analysis.")
        return

    # Creating interaction terms
    for genre_col in genre_columns:
        for mood_col in mood_columns:
            interaction_col_name = f'{genre_col}_{mood_col}_interaction'
            df[interaction_col_name] = df[genre_col] * df[mood_col]
            
    X_columns = genre_columns + mood_columns + [f'{g}_{m}_interaction' for g in genre_columns for m in mood_columns]
    X = sm.add_constant(df[X_columns])  # Add a constant term for the intercept
    
    y_overall = df['overall_rating']

    """
    print("\nX Matrix:")
    print(X.head())  # Print the first few rows of the X matrix for debugging
    """

    try:
        model_overall = sm.OLS(y_overall, X).fit()
        print("\nRegression Analysis Summary for Overall Rating:")
        print(model_overall.summary())
    except Exception as e:
        print("\nError occurred during regression analysis:")
        print(e)  # Print the error message for debugging


def elbow_cluster_printing(df_music_features, df):
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_music_features)

    # Finding the optimal number of clusters using the Elbow Method
    inertia = []
    for i in range(1, 22):
        kmeans = KMeans(n_clusters=i,n_init=10, random_state=42)
        kmeans.fit(df_scaled)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(12, 6))
    plt.plot(range(1, 22), inertia, marker='o', linestyle='--')
    plt.title('Elbow Method')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')

    # Save the plot to a file
    # plt.savefig('elbow_ratings_dropped_plot.png')

    optimal_clusters = 17  # Update this based on the Elbow plot

    # Apply K-means Clustering
    kmeans = KMeans(n_clusters=optimal_clusters, n_init=10, random_state=42)
    df['Cluster'] = kmeans.fit_predict(df_scaled)

    # Explore the cluster assignments
    print(df['Cluster'].value_counts())

    centroids = kmeans.cluster_centers_
    centroids_original_scale = scaler.inverse_transform(centroids)
    df_centroids = pd.DataFrame(centroids_original_scale, columns=df_music_features.columns)

    filtered_centroids = df_centroids[df_centroids['overall_rating'] >= 2.0]
    return filtered_centroids

def perform_association_rule_mining(df, min_support=0.01, metric="confidence", min_threshold=0.8):
    """
    Performs association rule mining on given DataFrame.
    
    Parameters:
    - df: DataFrame where each row represents a song with discretized attributes as columns.
          Columns are expected to be one-hot encoded for presence of each discretized attribute level.
    - min_support: Minimum support for the apriori algorithm.
    - metric: Metric to evaluate if a rule is significant (default: "confidence").
    - min_threshold: Minimum threshold for the metric to consider a rule significant.
    """
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    
    # Generate association rules
    rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)
    
    # Filter rules based on some criteria, e.g., high lift and confidence
    significant_rules = rules[(rules['lift'] >= 1) & (rules['confidence'] >= 0.8)]
    
    return significant_rules


@main.route("/test_results", methods=['GET'])
@login_required
def test_results():
    test_id = request.args.get('testId')
    user = current_user
    test = Test.query.filter_by(id=test_id).first()

    if test.subject != current_user: 
        return jsonify({'error': 'User does not match test owner'}), 403

    test_answers = UserAnswer.query.filter_by(user=user, test_id=test.id).all()
    structured_data = prepare_structured_data(test_answers)
    df = pd.DataFrame(structured_data)
    #rating_columns = ['overall_rating', 'genre_rating', 'mood_rating', 'vocal_timbre_rating']
    rating_columns = ['overall_rating']
    genre_columns = ['Rock', 'Hip Hop', 'Pop Ballad', 'Electronic', 'Jazz', 'Korean Ballad', 'R&B/Soul']
    mood_columns = ['Emotional', 'Tense', 'Bright', 'Relaxed']
    vocal_columns = ['Smooth', 'Dreamy', 'Raspy']
    # Note: 'Voiceless' is intentionally excluded based on your requirement

    ### CORRELATION COEFFICIENT ###
    calculate_significant_correlations_for_ratings(df, rating_columns, genre_columns, mood_columns, vocal_columns)
    
    ### REGRESSION ANALYSIS ###
    df = pd.DataFrame(structured_data)
    perform_regression_analysis(df, genre_columns, mood_columns)
    
    ### CLUSTERING ### 
    df = pd.DataFrame(structured_data)
    columns_to_drop = ['genre_rating', 'mood_rating', 'vocal_timbre_rating']  # Temporary
    df.drop(columns=columns_to_drop, inplace=True)

    data_columns = genre_columns + mood_columns + vocal_columns
    df_music_features = df[data_columns]
    
    #elbow_cluster_printing(df_music_features, df)

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_music_features)

    # Fit the KMeans algorithm to the scaled features
    kmeans = KMeans(n_clusters=7, n_init=10, random_state=42)
    kmeans.fit(scaled_features)

    # Predict the cluster for each song
    df['Cluster_Label'] = kmeans.predict(scaled_features)

    cluster_avg_rating = df.groupby('Cluster_Label')['overall_rating'].mean()

    # Determine if the user likes the songs in each cluster
    # Setting the threshold for 'like' as a positive average rating
    clusters_liked = cluster_avg_rating[cluster_avg_rating > 0]

    print("Clusters liked by the user (based on positive average rating):")
    print(clusters_liked)

    df = pd.DataFrame(structured_data)
    features_and_ratings_columns = rating_columns + genre_columns + mood_columns + vocal_columns
    df_features_and_ratings = df[features_and_ratings_columns]
    high_rated_clusters = elbow_cluster_printing(df_features_and_ratings, df)
    rating_rm_rows = high_rated_clusters.iloc[:, 1:]
    
    # creating dicitonary (key -> attribute column, value -> rating value)
    row_dicts = []
    # Iterate through each row in the DataFrame
    for index, row in rating_rm_rows.iterrows():
        # Create a dictionary for the current row
        row_dict = {}
        # Iterate through each column in the row
        for column, value in row.items():
            # Check if the value is above 0.05
            if value > 0.05:
                row_dict[column] = value
        # Append the dictionary to the list
        row_dicts.append(row_dict)

    # Print the list of dictionaries
    for row_dict in row_dicts:
        print(row_dict)

    #take me to query_open_ai route that inputs dictionary through open ai

    """
    scaler = StandardScaler()
    scaled_features_and_ratings = scaler.fit_transform(df_features_and_ratings)
    kmeans_with_ratings = KMeans(n_clusters=7, random_state=42)
    kmeans_with_ratings.fit(scaled_features_and_ratings)

    df['Cluster_With_Ratings'] = kmeans_with_ratings.predict(scaled_features_and_ratings)

    # Print out the first few entries to see the new cluster assignments
    print(df[['overall_rating', 'Cluster_With_Ratings']].head())
    """

    ### ASSOCIATE RULE MINING ###
    """ need to create df_transformed beforehand.
    significant_rules = perform_association_rule_mining(df_transformed, min_support=0.05, metric="lift", min_threshold=1.2)
    print("Significant Association Rules:")
    print(significant_rules)
    """
    response_data = {
        'user_id': user.id,
        'test_id': test.id,
        'test_type': test.test_type,
        'structured_data': structured_data
    }
    return jsonify(response_data)