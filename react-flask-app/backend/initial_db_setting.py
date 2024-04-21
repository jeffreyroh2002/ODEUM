from api import db, create_app
import os
import json

#import scripts that use ML model
from api.pred_scripts.predict_genre import predict_genre
from api.pred_scripts.predict_mood import predict_mood
from api.pred_scripts.predict_timbre import predict_timbre
from api.models import AudioFile

# path for predicting genre, mood, timbre


genre_saved_mfcc = os.path.join(os.getcwd(), 'api', 'static', 'mfccs', 'tmp', 'full-audio.json')
mood_saved_mfcc = os.path.join(os.getcwd(), 'api', 'static', 'mfccs', 'tmp', 'instrumental-audio.json')
timbre_saved_mfcc = os.path.join(os.getcwd(), 'api', 'static', 'mfccs', 'tmp', 'vocal-audio.json')

genre_model_path = os.path.join(os.getcwd(), 'api', 'mlModels', '0109_PCRNN_Genre7_final_100each_100ep_0.00001lr', 'best_model.h5')
mood_model_path = os.path.join(os.getcwd(), 'api', 'mlModels', 'pred_mood', 'saved_model')
timbre_model_path = os.path.join(os.getcwd(), 'api', 'mlModels', 'pred_vocal', 'saved_model')

def prepare_prediction_models():
    if not os.path.exists(genre_saved_mfcc) or not os.path.exists(mood_saved_mfcc) \
        or not os.path.exists(timbre_saved_mfcc):
        raise FileNotFoundError("please generate your json(of mfcc) files before you use prediction models")

    if not os.path.exists(genre_model_path) or not os.path.exists(mood_model_path) \
        or not os.path.exists(timbre_model_path):
        raise FileNotFoundError("please generate your mlModels")

def analyze_audio_data():
    # Save audio files into DB
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        from api.models import AudioFile

        full_mix_dir = '../../data_preprocessing/split_audio/full-audio'
        instrumental_mix_dir = '../../data_preprocessing/split_audio/instrumental-audio'
        timbre_mix_dir = '../../data_preprocessing/split_audio/vocal-audio'

        # Predict and save genre, mood, and timbre data
        genre_data = predict_genre(genre_model_path, genre_saved_mfcc)
        mood_data = predict_mood(mood_model_path, mood_saved_mfcc)
        timbre_data = predict_timbre(timbre_model_path, timbre_saved_mfcc)

        # Set default timbre values
        default_timbre_data = {'Smooth': 0.0, 'Dreamy': 0.0, 'Raspy': 0.0, 'Voiceless': 1.0}


        # Iterate through the full mix directory
        for full_mix_file_name in os.listdir(full_mix_dir):
            full_mix_file_path = os.path.join(full_mix_dir, full_mix_file_name)

            # Extract first 5 characters from full mix name
            audio_name_prefix = full_mix_file_name[:8]

            # Find a match in the data dictionaries based on the audio file name prefix
            relevant_genre_data = next((data for key, data in genre_data.items() if key.startswith(audio_name_prefix)), {})
            relevant_mood_data = next((data for key, data in mood_data.items() if key.startswith(audio_name_prefix)), {})
            relevant_timbre_data = next((data for key, data in timbre_data.items() if key.startswith(audio_name_prefix)), {})
            
            # If relevant_timbre_data is available, replace the default value
            if not relevant_timbre_data:
                relevant_timbre_data = default_timbre_data

            # Convert data to JSON format
            genre_data_json = json.dumps(relevant_genre_data)
            mood_data_json = json.dumps(relevant_mood_data)

            timbre_data_json = json.dumps(relevant_timbre_data)

            dominant_genre = max(relevant_genre_data, key=relevant_genre_data.get)
            dominant_mood = max(relevant_mood_data, key=relevant_mood_data.get)
            dominant_vocal = max(relevant_timbre_data, key=relevant_timbre_data.get)

            # Create an instance of AudioFile and add it to the database session
            audio_file = AudioFile(
                audio_name=full_mix_file_name,
                file_path=full_mix_file_path,
            )
            # Set the genre, mood, and vocal properties using their setter methods
            audio_file.genre = relevant_genre_data
            audio_file.mood = relevant_mood_data
            audio_file.vocal = relevant_timbre_data

            audio_file.dominant_genre = dominant_genre
            audio_file.dominant_mood = dominant_mood
            audio_file.dominant_vocal = dominant_vocal

            # Add the audio file to the database session
            db.session.add(audio_file)

        # Commit the changes to the database
        db.session.commit()

if __name__ == "__main__":
    prepare_prediction_models()
    analyze_audio_data()