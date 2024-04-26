from api import db, create_app
from api.models import AudioFile

from google.cloud import storage
import json

def initialize_audio_database():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
    
        storage_client = storage.Client.from_service_account_json('/workspace/ODEUM/react-flask-app/backend/api/odeum-421210-44f51ed247e8.json')
        bucket = storage_client.get_bucket("odeum-musics")
        
        model_output_json_path = "model_output.json"
        blob = bucket.blob("model_output/" + model_output_json_path)
        blob.download_to_filename(model_output_json_path)

        genre_columns = ['Rock', 'Hip Hop', 'Pop Ballad', 'Electronic', 'Jazz', 'Korean Ballad', 'R&B/Soul']
        mood_columns = ['Emotional', 'Tense', 'Bright', 'Relaxed']
        vocal_columns = ['Smooth', 'Dreamy', 'Raspy', 'Voiceless']

        with open(model_output_json_path, 'r') as file:
            model_output = json.load(file)

            for audio_name, value in model_output.items():
                genre_data = {label: score for label, score in value.items() if label in genre_columns}
                mood_data = {label: score for label, score in value.items() if label in mood_columns}
                vocal_data = {label: score for label, score in value.items() if label in vocal_columns}
                
                audio_file = AudioFile(
                    audio_name = audio_name,
                    genre = json.dumps(genre_data),
                    mood = json.dumps(mood_data),
                    vocal = json.dumps(vocal_data),
                    dominant_genre = max(genre_data, key=genre_data.get),
                    dominant_mood = max(mood_data, key=mood_data.get),
                    dominant_vocal = max(vocal_data, key=vocal_data.get)
                )
                db.session.add(audio_file)
            
            db.session.commit()
            audiofiles = AudioFile.query.all()
            print(audiofiles)
    

if __name__ == "__main__":
    initialize_audio_database()



# initial_db_setting.py 에는 이 저장된 json 파일을 하나씩 읽으면서 불러오고 AudioFile 객체로 저장
# 마지막으로 잘 저장되었는지 확인하는 함수를 만들기
