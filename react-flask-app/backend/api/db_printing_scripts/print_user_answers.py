from api.models import User, UserAnswer, AudioFile, Test
from api import db, create_app

app = create_app()
with app.app_context():
    current_user = User.query.order_by(User.id.asc()).first()
    print("current user:", current_user)
    answers = current_user.answers
    for answer in answers:
        audio_id = answer.audio_id
        audio = AudioFile.query.filter_by(id=audio_id).first()
        if (audio != None):
            print("song: ", audio)
            print("overall rating:", answer.rating)
