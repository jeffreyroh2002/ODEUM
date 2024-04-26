from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from api import db, login_manager
from flask_login import UserMixin
import openai
from sqlalchemy.ext.hybrid import hybrid_property
import json


openai.api_key = ''


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
        return f"User('{self.first_name}', '{self.email}')"


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_type = db.Column(db.Integer, nullable=False)
    test_start_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    test_end_time = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    pre_survey_data = db.Column(db.Text)  # Using Text to store JSON-formatted string
    liked_artists = db.Column(db.Text)
    answers = db.relationship("UserAnswer", backref="test", lazy=True)


    def __repr__(self):
        return f"Test(user_id={self.user_id}, id={self.id}, test_type={self.test_type}, start_time={self.test_start_time}, end_time={self.test_end_time})"


    @property
    def decoded_pre_survey_answers(self):
        return json.loads(self.pre_survey_answers)

    @decoded_pre_survey_answers.setter
    def decoded_pre_survey_answers(self, value):
        self.pre_survey_answers = json.dumps(value)

### NEED TO CHANGE genre, mood, vocal to non-text,  adding serialization and deserialization 
### methods to ease the process of working with these fields in Python as dictionaries
"""
Consider Adding Utility Methods: 
For complex data like your JSON fields, utility methods in the models that parse these 
fields into a more usable format for analysis can save time. For example, methods that 
return the genre, mood, and vocal data as a Python dictionary directly could be beneficial.

GPT4 -> advice READ!
"""

class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    audio_name = db.Column(db.String(50), nullable=False)
    genre = db.Column('genre', db.Text, nullable=False)
    mood = db.Column('mood', db.Text, nullable=False)
    vocal = db.Column('vocal', db.Text, nullable=False)
    dominant_genre = db.Column(db.String(15), nullable=False)
    dominant_mood = db.Column(db.String(15), nullable=False)
    dominant_vocal = db.Column(db.String(15), nullable=False)

    answers = db.relationship("UserAnswer", backref="audio", lazy=True)

    @hybrid_property
    def genre(self):
        return json.loads(self._genre)

    @hybrid_property
    def mood(self):
        return json.loads(self._mood)

    @hybrid_property
    def vocal(self):
        return json.loads(self._vocal)

    def __repr__(self):
        return f"AudioFile('{self.audio_name}', 'genre:{self.genre}', 'mood:{self.mood}', 'timbre:{self.vocal}')"
        return f"AudioFile('{self.audio_name}')"

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    overall_rating = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    audio_id = db.Column(db.Integer, db.ForeignKey("audio_file.id"), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey("test.id"), nullable=False)
    question_index = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return (
            f"UserAnswer('rating:{self.overall_rating}')"
        )

#currently am not using the presurveyanswer model. Better to use this than plain text in Test model#
class PreSurveyAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    _answers = db.Column('answers', db.Text, nullable=False)  # Using Text for flexibility; JSON for PostgreSQL
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    test = db.relationship('Test', backref=db.backref('pre_survey_associations', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('user_pre_survey_answers', lazy='dynamic'))

    @property
    def answers(self):
        return json.loads(self._answers)

    @answers.setter
    def answers(self, value):
        self._answers = json.dumps(value)

    def __repr__(self):
        return f"<PreSurveyAnswer(test_id={self.test_id}, user_id={self.user_id}, question_id={self.question_id}, answers={self._answers})>"