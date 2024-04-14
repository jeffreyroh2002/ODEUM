import os
import re

uri = os.getenv('DATABASE_URL')
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)  # Only replace the first occurrence

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '9a96279c05c8abc02388d6faba5654f5')
    SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///site.db'
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('REDIRECT_URI', 'https://jeffreyroh2002-odeum-ol6y5xcofwj.ws-us110.gitpod.io/callback')

    @staticmethod
    def init_app(app):
        if not Config.SPOTIFY_CLIENT_ID or not Config.SPOTIFY_CLIENT_SECRET:
            raise ValueError("Spotify credentials must be set")