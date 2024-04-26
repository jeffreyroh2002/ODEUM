import sys
import os
import librosa
import json
import math

from pydub import AudioSegment
from datetime import datetime  # Import the datetime module

from google.cloud import storage

from pred_scripts.predict_genre import predict_genre
from pred_scripts.predict_mood import predict_mood
from pred_scripts.predict_timbre import predict_timbre

SAMPLE_RATE = 22050
DURATION = 30
SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION

def count_audios(directory):
    with os.scandir(directory) as entries:
        return sum(1 for entry in entries if entry.is_file())

def split_wav_into_segments():
    print(os.getcwd())
    #a directory of full-length audios 
    non_split_audio_directory = os.path.join("non_split_audio")
    if not os.path.exists(non_split_audio_directory):
        raise FileNotFoundError("non split audio path does not exist")

    #a directory where we split audios
    split_audio_directory = os.path.join("split_audio")
    os.makedirs(split_audio_directory, exist_ok=True)

    timestamps_path = os.path.join("timestamps.txt")
    if not os.path.exists(timestamps_path):
        raise FileNotFoundError("timestamps file does not exist")

    full_audio_directory = os.path.join(non_split_audio_directory, "full-audio")
    instrumental_audio_directory = os.path.join(non_split_audio_directory, "instrumental-audio")
    vocal_audio_directory = os.path.join(non_split_audio_directory, "vocal-audio")

    # Ensure the length of the txt file and the num audios are equal
    with open(timestamps_path, 'r') as file:
        line_count = sum(1 for line in file)

    full_audio_count = count_audios(full_audio_directory)
    instrumental_audio_count = count_audios(instrumental_audio_directory)
    vocal_audio_count = count_audios(vocal_audio_directory)

    assert full_audio_count == instrumental_audio_count and full_audio_count == vocal_audio_count \
           and full_audio_count == line_count

    # Read the input file and process each line 
    with open(timestamps_path, "r") as timestamps:
        for timestamp in timestamps:
            data = timestamp.strip().split(",")
            song_name, start_time, end_time = data[0], int(data[1]) * 1000, int(data[2]) * 1000
            print(song_name, start_time, end_time)
            
            for audio_type in ["full-audio", "instrumental-audio", "vocal-audio"]:
                audio_path = os.path.join(non_split_audio_directory, audio_type, song_name)
                try:
                    audio = AudioSegment.from_wav(audio_path)
                except:
                    print(f"an error occurred when getting audio {song_name}")
                
                segment = audio[start_time:end_time]
                
                output_path = os.path.join(split_audio_directory, audio_type)
                os.makedirs(output_path, exist_ok=True)
                
                output_file = os.path.join(output_path, song_name)
        
                segment.export(output_file, format="wav")



def before_preprocessing():
    full_audio_path = 'non_split_audio/full-audio/'
    instrumental_audio_path = 'non_split_audio/instrumental-audio'
    vocal_audio_path = 'non_split_audio/vocal-audio'

    assert len(os.listdir(full_audio_path)) == len(os.listdir(instrumental_audio_path)) == len(os.listdir(vocal_audio_path))

def upload_audio_to_gcs():
    storage_client = storage.Client.from_service_account_json('/workspace/ODEUM/react-flask-app/backend/api/odeum-421210-44f51ed247e8.json')
    bucket = storage_client.get_bucket("odeum-musics")
    
    audio_path = "split_audio/"
    for audio_type in ["full-audio/", "instrumental-audio/", "vocal-audio/"]:
        audios = os.listdir(audio_path + audio_type)
        for audio in audios:
            blob = bucket.blob('audios/' + audio_type + audio)
            blob.upload_from_filename(audio_path + audio_type + audio)

def upload_mfccs_to_gcs():
    storage_client = storage.Client.from_service_account_json('/workspace/ODEUM/react-flask-app/backend/api/odeum-421210-44f51ed247e8.json')
    bucket = storage_client.get_bucket("odeum-musics")

    gcs_audio_path = "audios/"
    tmp_filename = "tmp.wav"
    num_segments= 10

    for audio_type in ["full-audio", "instrumental-audio", "vocal-audio"]:
        data = {
            "mapping": [],
            "mfcc": [],
            "labels": [],
            "filenames": []  # Store the file names
        }
        blobs = storage_client.list_blobs("odeum-musics", prefix = gcs_audio_path + audio_type)
        for blob in blobs:
            audio_filename = blob.name.split('/')[-1]
            blob.download_to_filename(tmp_filename)
            signal, sr = librosa.load(tmp_filename, sr=22050)
            length = int(signal.shape[0]/float(sr))  # measured in seconds for GTZAN Dataset
            num_samples_per_segment = int(SAMPLES_PER_TRACK / num_segments) # here, int(22050 * 30 / 5)
            expected_num_mfcc_vectors_per_segment = math.ceil(num_samples_per_segment / 512)
            # process segments extracting mfcc and storing data
            for s in range(num_segments):
                start_sample = num_samples_per_segment * s
                finish_sample = start_sample + num_samples_per_segment
                mfcc = librosa.feature.mfcc(y=signal[start_sample:finish_sample],
                                            sr=22050,
                                            n_fft=2048,
                                            n_mfcc=13,
                                            hop_length=512)
                mfcc = mfcc.T
                if len(mfcc) == expected_num_mfcc_vectors_per_segment:
                    data["mfcc"].append(mfcc.tolist())  # convert numpy array to list
                    data["labels"].append(0)
                    data["filenames"].append(audio_filename)  # fixed this line
                    print("{}, segment:{}".format(audio_filename, s))

            if length != 30 and length == 60 :  # the case that an audio file is 60 secs long
                for s in range(num_segments, num_segments*2):
                    start_sample = num_samples_per_segment * s
                    finish_sample = start_sample + num_samples_per_segment
                    mfcc = librosa.feature.mfcc(y=signal[start_sample:finish_sample],
                                                    sr=22050,
                                                    n_fft=2048,
                                                    n_mfcc=13,
                                                    hop_length=512)
                    mfcc = mfcc.T

                    # store mfcc for a segment if it has the expected length
                    if len(mfcc) == expected_num_mfcc_vectors_per_segment:
                        data["mfcc"].append(mfcc.tolist())  # convert numpy array to list
                        data["labels"].append(0)
                        data["filenames"].append(audio_filename)  # fixed this line
                        print("{}, segment:{}".format(audio_filename, s))
            
            elif length != 30 :
                print(f"Error : {audio_filename}")  

            os.remove(tmp_filename)    

        output_filename = audio_type + ".json"
        with open(output_filename, 'w') as fp:
            json.dump(data, fp, indent=4)
        
        blob = bucket.blob("mfccs/" + output_filename)
        blob.upload_from_filename(output_filename)

        os.remove(output_filename)

def upload_model_output_json_to_gcs():
    storage_client = storage.Client.from_service_account_json('/workspace/ODEUM/react-flask-app/backend/api/odeum-421210-44f51ed247e8.json')
    bucket = storage_client.get_bucket("odeum-musics")

    gcs_mfcc_path = "mfccs/"
    gcs_json_path = "model_output.json"
    tmp_mfcc_filename = "tmp.json"
    model_output_json_path = "model_output.json"

    genre_model_path = os.path.join(os.getcwd(), 'mlModels', 'pred_genre', 'best_model.h5')
    mood_model_path = os.path.join(os.getcwd(), 'mlModels', 'pred_mood', 'saved_model')
    timbre_model_path = os.path.join(os.getcwd(), 'mlModels', 'pred_vocal', 'saved_model')

    # Save filenames in gcs
    filenames = [file.name[18:] for file in list(bucket.list_blobs(prefix="audios/full-audio/"))]
    
    # Initialize json file that will be uploaded to gcs
    model_output_json = {filename: {} for filename in filenames}

    # Set default timbre values
    default_timbre_data = {'Smooth': 0.0, 'Dreamy': 0.0, 'Raspy': 0.0, 'Voiceless': 1.0}

    for predict_type in ["genre", "mood", "timbre"]:
        model_path = locals()[f"{predict_type}_model_path"]
        predict_function = globals()[f"predict_{predict_type}"]
        if predict_type == "genre": mfcc_path = gcs_mfcc_path + "full-audio.json"
        elif predict_type == "mood": mfcc_path = gcs_mfcc_path + "instrumental-audio.json"
        else: mfcc_path = gcs_mfcc_path + "vocal-audio.json"

        blob = bucket.blob(mfcc_path)
        blob.download_to_filename(tmp_mfcc_filename)

        predicted_data = predict_function(model_path, tmp_mfcc_filename)

        for filename in filenames:
            relevant_data = next((content for key, content in predicted_data.items() if key.startswith(filename.split(".")[0])), {})
            
            if predict_type == "timbre" and not relevant_data:
                relevant_data = default_timbre_data
            
            model_output_json[filename].update(relevant_data)
        
    with open(model_output_json_path, 'w') as f:
        json.dump(model_output_json, f, indent=4)
    
    blob = bucket.blob("model_output/" + model_output_json_path)
    blob.upload_from_filename(model_output_json_path)

    os.remove(model_output_json_path)

        

if __name__ == "__main__":
    # before_preprocessing()
    # split_wav_into_segments()
    # upload_audio_to_gcs()
    # upload_mfccs_to_gcs()
    upload_model_output_json_to_gcs()

