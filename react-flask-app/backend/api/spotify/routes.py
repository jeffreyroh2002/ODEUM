from flask import Flask, Blueprint, request, redirect, session, url_for, current_app, jsonify
from api import db, login_manager
from api.models import User, AudioFile, UserAnswer, Test
import requests
import os
import base64
import json
from flask_login import login_required, current_user 

spotify = Blueprint('spotify', __name__)

def get_spotify_token():
    """ Retrieves Spotify access token using Client Credentials flow. """
    client_id = current_app.config['SPOTIFY_CLIENT_ID']
    client_secret = current_app.config['SPOTIFY_CLIENT_SECRET']
    response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={'grant_type': 'client_credentials'},
        headers={'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()}
    )
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        spotify.logger.error(f"Failed to retrieve Spotify access token: {response.json()}")
        return None

@spotify.route('/get-token')
def send_token():
    """ Sends Spotify access token as JSON. """
    token = get_spotify_token()
    if token:
        return jsonify({'access_token': token})
    else:
        return jsonify({'error': 'Failed to retrieve access token'}), 500

@spotify.route('/login_spotify')
def login_spotify():
    """ Redirects to Spotify's authorization URL. """
    scope = "user-read-private user-read-email"
    return redirect(
        f"https://accounts.spotify.com/authorize?response_type=code&client_id={current_app.config['SPOTIFY_CLIENT_ID']}"
        f"&scope={scope}&redirect_uri={current_app.config['REDIRECT_URI']}"
    )

@spotify.route('/callback_spotify')
def callback():
    """ Handles callback from Spotify OAuth, fetches access token. """
    code = request.args.get('code')
    if not code:
        return "Authorization failed, no code provided.", 400

    token_url = 'https://accounts.spotify.com/api/token'
    client_credentials = f"{current_app.config['SPOTIFY_CLIENT_ID']}:{current_app.config['SPOTIFY_CLIENT_SECRET']}"
    client_credentials_b64 = base64.b64encode(client_credentials.encode()).decode()

    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': current_app.config['REDIRECT_URI']
    }
    token_headers = {
        'Authorization': f"Basic {client_credentials_b64}"
    }
    response = requests.post(token_url, data=token_data, headers=token_headers)
    if response.status_code != 200:
        return f"Failed to retrieve access token: {response.content}", response.status_code

    access_token = response.json().get('access_token')
    if not access_token:
        return "Authorization failed, no access token provided.", 400

    session['access_token'] = access_token
    return redirect(url_for('main.index'))

@spotify.route('/fetch-popular-artists', methods=['GET'])
def fetch_popular_artists():
    """ Fetches popular artists across specified genres and markets. """
    genres = ['pop', 'rock', 'hip-hop', 'jazz', 'electronic', 'rnb', 'indie']
    markets = ['US', 'KR']
    token = get_spotify_token()
    if not token:
        return jsonify({'error': 'Failed to authenticate with Spotify'}), 500

    all_artists = []
    artist_ids = set()

    try:
        for market in markets:
            for genre in genres:
                response = requests.get(
                    'https://api.spotify.com/v1/search',
                    headers={'Authorization': f'Bearer {token}'},
                    params={
                        'q': f'genre:"{genre}"',
                        'type': 'artist',
                        'market': market,
                        'limit': 2
                    }
                )
                if response.status_code == 200:
                    artists = response.json()['artists']['items']
                    for artist in artists:
                        if artist['id'] not in artist_ids:
                            artist_ids.add(artist['id'])
                            all_artists.append(artist)
                else:
                    spotify.logger.error(f"Error fetching artists for {genre} in {market}: {response.json()}")
    except Exception as e:
        spotify.logger.error(f"Exception during artist fetch: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

    sorted_artists = sorted(all_artists, key=lambda x: x['popularity'], reverse=True)[:20]
    formatted_artists = [{
        'id': artist['id'],
        'name': artist['name'],
        'imageUrl': artist['images'][0]['url'] if artist['images'] else None,
        'popularity': artist['popularity']
    } for artist in sorted_artists]

    return jsonify(formatted_artists)

@spotify.route('/submit_artists', methods=['POST'])
@login_required
def submit_artists():
    try:
        data = request.get_json()
        artist_ids = data.get('selectedArtistIds', [])
        test = Test.query.filter_by(user_id=current_user.id).order_by(Test.test_start_time.desc()).first()
        if test is not None:
            test.liked_artists = json.dumps(artist_ids)
            # Serialize and save back to the test
            db.session.commit()
            print("Here is what is commited to DB!!!:", test.liked_artists)
            return jsonify({"message": "Liked Artists updated successfully!", "test_id": test.id}), 200
        else:
            return jsonify({"error": "No test found for the user"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400