from flask import Blueprint, request, redirect, session, url_for
import requests
import os

spotify = Blueprint('spotify', __name__)

@spotify.route('/login_spotify')
def login_spotify():
    scope = "user-read-private user-read-email"
    return redirect(
        f"https://accounts.spotify.com/authorize?response_type=code&client_id={current_app.config["SPOTIFY_CLIENT_ID"]}"
        f"&scope={scope}&redirect_uri={current_app.config["REDIRECT_URI"]}"
    )

@main.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': current_app.config["REDIRECT_URI"]
    }
    token_headers = {
        'Authorization': f"Basic {current_app.config["SPOTIFY_CLIENT_SECRET"]}"  # You should base64 encode 'client_id:client_secret'
    }
    r = requests.post(token_url, data=token_data, headers=token_headers)
    access_token = r.json().get('access_token')
    session['access_token'] = access_token  # Store the token in session or a more persistent storage
    return redirect(url_for('main.index'))