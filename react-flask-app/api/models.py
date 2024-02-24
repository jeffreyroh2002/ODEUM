from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from api import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=True)
    tests = db.relationship("Test", backref="subject", lazy=True)
    answers = db.relationship("UserAnswer", backref="user", lazy=True)

    def get_reset_token(self, expires_sec=600):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_type = db.Column(db.Integer, nullable=False)
    test_start_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    test_end_time = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    answers = db.relationship("UserAnswer", backref="test", lazy=True)


    def __repr__(self):
        return f"Test('user:{self.user_id}', 'test:{self.test_type}', '{self.test_start_time}', '{self.test_end_time}')"


class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    audio_name = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.Text, nullable=False)  # save with json.dump
    mood = db.Column(db.Text, nullable=False)
    vocal = db.Column(db.Text, nullable=False)
    answers = db.relationship("UserAnswer", backref="audio", lazy=True)

    def __repr__(self):
        return f"AudioFile('{self.audio_name}', '{self.file_path}', 'genre:{self.genre}', 'mood:{self.mood}', 'timbre:{self.vocal}')"


class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    overall_rating = db.Column(db.Integer, nullable=False)
    genre_rating = db.Column(db.Integer, nullable=True)
    mood_rating = db.Column(db.Integer, nullable=True)
    vocal_timbre_rating = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    audio_id = db.Column(db.Integer, db.ForeignKey("audio_file.id"), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey("test.id"), nullable=False)

    def __repr__(self):
        return (
            f"UserAnswer('user:{self.user_id}', 'test:{self.test_id}' 'audio:{self.audio_id}', 'rating:{self.overall_rating}')"
        )
