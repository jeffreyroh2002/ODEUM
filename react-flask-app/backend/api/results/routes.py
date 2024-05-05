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

    print(correlation_matrix)
    
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
    
    y_overall = df['rating']

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

def get_high_rated_clusters(df_music_features, optimal_clusters, df):
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_music_features)
    
    num_clusters = optimal_clusters
    kmeans = KMeans(n_clusters=num_clusters, n_init=10, random_state=42)
    df['Cluster'] = kmeans.fit_predict(df_scaled)

    print(df['Cluster'].value_counts())

    centroids = kmeans.cluster_centers_
    centroids_original_scale = scaler.inverse_transform(centroids)
    df_centroids = pd.DataFrame(centroids_original_scale, columns=df_music_features.columns)

    filtered_centroids = df_centroids[df_centroids['rating'] >= 2.0]
    return df_centroids, filtered_centroids

def get_user_preferred_clusters(df_music_features, optimal_clusters, df):
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_music_features)

    # Fit the KMeans algorithm to the scaled features
    kmeans = KMeans(n_clusters=optimal_clusters, n_init=10, random_state=42)
    kmeans.fit(scaled_features)

    # Predict the cluster for each song
    df['Cluster_Label'] = kmeans.predict(scaled_features)

    cluster_avg_rating = df.groupby('Cluster_Label')['rating'].mean()

    # Determine if the user likes the songs in each cluster
    # Setting the threshold for 'like' as a positive average rating
    clusters_liked = cluster_avg_rating[cluster_avg_rating > 0]

    print("Clusters liked by the user (based on positive average rating):")
    print(clusters_liked)

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


def request_open_ai(test):
    llm = ChatOpenAI(openai_api_key="my-openai-api-key", temperature=0, model_name='gpt-3.5-turbo')
    my_question= ""
    ai_response = (llm([HumanMessage(content=my_question)]))
    print(ai_response)
    return(ai_response)


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
    df_centroids, high_rated_clusters = get_high_rated_clusters(df_features_and_ratings, 7, df)
    print(df_centroids)
    get_user_preferred_clusters(df_features_and_ratings, 7, df)
    
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

    #take me to query_open_ai route that inputs dictionary through open ai


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