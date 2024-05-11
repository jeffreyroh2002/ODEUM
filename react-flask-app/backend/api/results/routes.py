from flask import Blueprint, request, session, redirect, url_for, jsonify
from api import db, bcrypt
from api.models import User, AudioFile, UserAnswer, Test
#from api.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_wtf.csrf import generate_csrf
from flask_login import login_user, current_user, logout_user, login_required
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

from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import openai

#imports for saving png files
import io
import base64
from flask import render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator
from collections import defaultdict
import seaborn as sns
import os

results = Blueprint('results', __name__)

llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'), max_tokens=2048, temperature=0, model_name='gpt-3.5-turbo')

def prepare_structured_data(test_answers):
    """Extracts and structures data from test answers."""
    structured_data = []
    for answer in test_answers:
        audio = AudioFile.query.filter_by(id=answer.audio_id).first()
        if audio:
            data_row = {
                "rating": answer.rating,
                **audio.genre,
                **audio.mood,
                **audio.vocal
            }
            structured_data.append(data_row)
    return structured_data

def create_user_ratings_df(test_answers):
    """Creates a DataFrame from test answers containing user ratings."""
    user_ratings = pd.DataFrame([
        {'user_id': answer.user_id, 'song_id': answer.audio_id, 'rating': answer.rating}
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

    #print("\nAverage Ratings by Cluster:")
    #print(avg_ratings_by_cluster.head())

    # Analyze which clusters are rated more positively on average
    for cluster_num in range(n_clusters):
        cluster_avg_rating = avg_ratings_by_cluster[avg_ratings_by_cluster['cluster'] == cluster_num]['rating'].mean()
        #print(f"Cluster {cluster_num} Average Rating: {cluster_avg_rating}")

    # Further analysis can be done based on the findings
    liked_clusters = avg_ratings_by_cluster[avg_ratings_by_cluster['rating'] > 0].groupby('cluster')['rating'].mean()
    disliked_clusters = avg_ratings_by_cluster[avg_ratings_by_cluster['rating'] < 0].groupby('cluster')['rating'].mean()

def analyze_cluster_characteristics(df_clustered, n_clusters):
    """Analyzes the characteristics of each cluster."""
    cluster_characteristics = {}
    
    for cluster_label in range(n_clusters):
        cluster_data = df_clustered[df_clustered['cluster'] == cluster_label]
        cluster_centroid = cluster_data.mean()
        cluster_characteristics[cluster_label] = cluster_centroid
    
    return cluster_characteristics

def find_significant_correlations(correlation_matrix, threshold, columns):
    significant_pairs = []
    for column in columns:
        for index, value in correlation_matrix[column].items():
            # Check only one side of the diagonal to avoid duplicates
            if index > column and abs(value) >= threshold:
                # Ensure correlation meets threshold and is not self-correlation
                significant_pairs.append({
                    "Attribute 1": column,
                    "Attribute 2": index,
                    "Correlation": value
                })

    significant_correlations = pd.DataFrame(significant_pairs)
    return significant_correlations

def calculate_significant_correlations_for_ratings(df, rating_columns, genre_columns, mood_columns, vocal_columns, threshold=0.7):
    """Calculates and prints significant correlations for each rating type with relevant song attributes,
    ensuring there's sufficient variability in attributes for meaningful analysis."""
    correlation_matrix = df.corr()

    #print(correlation_matrix)
    
    # Exclude rating columns to focus on song attributes
    non_rating_columns = [col for col in df.columns if col not in rating_columns]
    
    # Ensure there's sufficient variability in attributes for meaningful analysis
    if len(non_rating_columns) <= len(rating_columns):
        print("Not enough variability in attributes for meaningful correlation analysis.")
        return
    
   # Since only 'overall_score' is used, directly relate it to all attributes
    overall_attributes = genre_columns + mood_columns + vocal_columns
    valid_attributes = [attr for attr in overall_attributes if attr in correlation_matrix.columns]

    # Calculate and print significant correlations for the overall rating with each valid attribute
    for attribute in valid_attributes:
        significant_correlations = find_significant_correlations(correlation_matrix, threshold, columns=[rating_columns[0], attribute])

        if not significant_correlations.empty:
            print(f"\nSignificant Correlations for {rating_columns[0]} with {attribute} (|correlation| >= {threshold}):\n", significant_correlations)
        else:
            print(f"\nNo significant correlations found for {rating_columns[0]} with {attribute} at the threshold of {threshold}.")

def perform_regression_analysis(df, genre_columns, mood_columns):
    """Performs regression analysis to model the impact of genre and mood on overall rating."""

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
    
    y_overall = df['rating']

    try:
        model_overall = sm.OLS(y_overall, X).fit()
        #print("\nRegression Analysis Summary for Overall Rating:")
        #print(model_overall.summary())
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

def get_high_rated_clusters(df_music_features, optimal_clusters, df):
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_music_features)
    
    num_clusters = optimal_clusters
    kmeans = KMeans(n_clusters=num_clusters, n_init=10, random_state=42)
    df['Cluster'] = kmeans.fit_predict(df_scaled)

    #print(df['Cluster'].value_counts())

    centroids = kmeans.cluster_centers_
    centroids_original_scale = scaler.inverse_transform(centroids)
    df_centroids = pd.DataFrame(centroids_original_scale, columns=df_music_features.columns)

    filtered_centroids = df_centroids[df_centroids['rating'] >= 1.5]
    return df_centroids, filtered_centroids

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

@results.route("/test_results", methods=['GET'])
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
    rating_columns = ['rating']
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
    data_columns = genre_columns + mood_columns + vocal_columns
    df_music_features = df[data_columns]
    
    # elbow_cluster_printing(df_music_features, df)

    df = pd.DataFrame(structured_data)
    features_and_ratings_columns = rating_columns + genre_columns + mood_columns + vocal_columns
    df_features_and_ratings = df[features_and_ratings_columns]

    # high rated clusters: filtering the centroids of the clusters directly based on a rating threshold. 
    # It filters the centroids to retain only those with ratings above a certain threshold.

    df_centroids, high_rated_clusters = get_high_rated_clusters(df_features_and_ratings, 7, df)
    #print(df_centroids)
    
    # creating dicitonary (key -> attribute column, value -> rating value)
    row_dicts = []
    # Iterate through each row in the DataFrame
    for index, row in high_rated_clusters.iterrows():
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

    df_centroids_rounded = df_centroids.round(2)
    clustering_data = df_centroids_rounded.to_dict()
    # df_centroids_rounded.to_csv('df_centroids.txt', sep='\t', index=False, float_format='%.2f')

    user = current_user
    
    test.clustering_output = json.dumps(clustering_data)
    survey_data = json.loads(test.pre_survey_data)
    
    if test.pre_survey_data:
        survey_data = json.loads(test.pre_survey_data)
        liked_genre = survey_data.get("3")
    else:
        liked_genre = "No info"

    clustering_info = json.dumps(json.loads(test.clustering_output), indent=2)

    # Connect to Open Ai API
    
    if test.gpt_analysis is None:
        # Common Requirements
        common_requirements = "refer to user as 'you', don't list traits, make the user learn something new, focus on the mixture of labels"
        prompt_intro = "With the following cluster info and genre preference, give analysis on user's music preference."
        cluster_details = f"Clustering Data: {clustering_info}"
        data_details = f"Clustering Data: {clustering_info}, liked genre: {liked_genre}"

        sub_prompts = [
            {
                "prompt": f"{prompt_intro} {cluster_details}",
                "requirements": f"sentences with nuanced description. {common_requirements}",
                "key": "description"
            },
            {
                "prompt": f"{prompt_intro} {cluster_details}",
                "requirements": f"sentences with high level description with analogies. {common_requirements}",
                "key": "analogies"
            },
            {
                "prompt": f"Suggest 3, nuanced songs that matches the cluster ratings and is preferably one of the user's liked genre, {data_details}",
                "requirements": f"be creative, songs that actually exist, don't have to be popular songs",
                "key": "recommendations"
            }
        ]

        complete_response = {}

        for sub_prompt in sub_prompts:
            try:
                # Simulate a call to a language model (replace this with actual API call)
                my_question = sub_prompt["prompt"] + ", " + sub_prompt["requirements"]
                ai_response = llm([HumanMessage(content=my_question)])
                ai_content = ai_response.content
                print("CHECKING HERE!!!", ai_content)
                complete_response[sub_prompt["key"]] = ai_content
            except Exception as e:
                print(f"Error during API call for {sub_prompt['key']}: {e}")
                complete_response[sub_prompt["key"]] = "Failed to generate response."

        # Combine all responses into a single text
        final_gpt_analysis = " ".join(complete_response.values())
        
        test.gpt_analysis = final_gpt_analysis

        try:
            db.session.commit()
            return jsonify({
                "message": "Analysis updated successfully!",
                "gpt_analysis": test.gpt_analysis
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({
            "message": "Loading already created info:",
            "gpt_analysis": test.gpt_analysis
        }), 200


    ### ASSOCIATE RULE MINING ###
    """ need to create df_transformed beforehand.
    significant_rules = perform_association_rule_mining(df_transformed, min_support=0.05, metric="lift", min_threshold=1.2)
    print("Significant Association Rules:")
    print(significant_rules)
    """
    """
    response_data = {
        'user_id': user.id,
        'test_id': test.id,
        'test_type': test.test_type,
        'structured_data': structured_data
    }
    return jsonify(response_data)
    """