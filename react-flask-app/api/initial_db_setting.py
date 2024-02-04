from WebApp import db, create_app
import os
import json

#import scripts that use ML model
from api.pred_scripts.predict_genre import predict_genre
from api.pred_scripts.predict_mood import predict_mood
from api.pred_scripts.predict_timbre import predict_timbre

# path for predicting genre, mood, timbre

"""
genre_saved_mfcc = os.path.join(os.getcwd(), 'api', 'static', 'mfccs', 'full_mix_mfcc.json')
mood_saved_mfcc = os.path.join(os.getcwd(), 'api', 'static', 'mfccs', 'instrumental_mfcc.json')
timbre_saved_mfcc = os.path.join(os.getcwd(), 'api', 'static', 'mfccs', 'vocal_mfcc.json')
"""
genre_saved_mfcc = os.path.join(os.getcwd(), 'api', 'static', 'mfccs', '3sample_mfccs.json')
mood_saved_mfcc = os.path.join(os.getcwd(), 'api', 'static', 'mfccs', '3sample_mfccs.json')
timbre_saved_mfcc = os.path.join(os.getcwd(), 'api', 'static', 'mfccs', '3sample_mfccs.json')

genre_model_path = os.path.join(os.getcwd(), 'api', 'mlModels', '0109_PCRNN_Genre7_final_100each_100ep_0.00001lr', 'best_model.h5')
mood_model_path = os.path.join(os.getcwd(), 'api', 'mlModels', 'pred_mood', 'saved_model')
timbre_model_path = os.path.join(os.getcwd(), 'api', 'mlModels', 'pred_vocal', 'saved_model')

app = create_app()

# Save audio files into DB
with app.app_context():
    db.drop_all()
    db.create_all()
    from api.models import AudioFile

    full_mix_dir = os.path.join(os.getcwd(), 'audio_data')
    instrumentals_dir = os.path.join(os.getcwd(), 'audio_data')
    vocals_dir = os.path.join(os.getcwd(), 'audio_data')

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

        # Convert data to JSON format
        genre_data_json = json.dumps(relevant_genre_data)
        mood_data_json = json.dumps(relevant_mood_data)
        timbre_data_json = json.dumps(default_timbre_data)
        
        # If relevant_timbre_data is available, replace the default values
        if relevant_timbre_data:
            timbre_data_json = json.dumps(relevant_timbre_data)

        # Create an instance of AudioFile and add it to the database session
        audio_file = AudioFile(
            audio_name=full_mix_file_name,
            file_path=full_mix_file_path,
            genre=genre_data_json,
            mood=mood_data_json,
            vocal=timbre_data_json
        )
        db.session.add(audio_file)

    # Commit the changes to the database
    db.session.commit()