from flask import Blueprint, request, redirect, session, url_for, current_app
import requests
import os
import base64

spotify = Blueprint('spotify', __name__)

@spotify.route('/login_spotify')
def login_spotify():
    scope = "user-read-private user-read-email"
    return redirect(
        f"https://accounts.spotify.com/authorize?response_type=code&client_id={current_app.config['SPOTIFY_CLIENT_ID']}"
        f"&scope={scope}&redirect_uri={current_app.config['REDIRECT_URI']}"
    )

@spotify.route('/callback_spotify')
def callback():
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

    session['access_token'] = access_token  # Store the token in session or a more persistent storage
    return redirect(url_for('main.index'))  # Make sure this endpoint is defined in your Flask application