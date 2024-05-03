import sys
import os
import librosa
import json
import math
import glob
import demucs.separate

from pydub import AudioSegment
from datetime import datetime  # Import the datetime module

from google.cloud import storage

from pred_scripts.predict_genre import predict_genre
from pred_scripts.predict_mood import predict_mood
from pred_scripts.predict_timbre import predict_timbre

SAMPLE_RATE = 22050
DURATION = 30
SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION

def convert_mp3_to_wav(mp3_file_path, wav_file_path):
    # Load the MP3 file
    audio = AudioSegment.from_mp3(mp3_file_path)
    
    # Export the audio data to a WAV file
    audio.export(wav_file_path, format="wav")
    
    os.remove(mp3_file_path)

def separate_audios_and_upload():
    audios = glob.glob("non_split_audio/full-audio/*")

    storage_client = storage.Client.from_service_account_json('/workspace/ODEUM/react-flask-app/backend/api/odeum-421210-44f51ed247e8.json')
    bucket = storage_client.get_bucket("odeum-musics")

    for audio_filepath in audios:
        #if the extension is ".mp3", converting it to ".wav"
        if audio_filepath[-4:] == ".mp3":
            convert_mp3_to_wav(audio_filepath, audio_filepath[:-4] + ".wav")
            audio_filepath = audio_filepath[:-4] + ".wav"

        #separating music into vocal/no_vocal with "Demucs"
        demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx", audio_filepath])
        
        #filename without extensions(.wav, .mp3 ...)
        audio_filename = audio_filepath.split('/')[-1][:-4]

        #paths of separated audios that will be saved later (yet, the extension is .mp3) 
        no_vocals_path = "separated/mdx/" + audio_filename + "/no_vocals.wav"
        vocals_path = "separated/mdx/" + audio_filename + "/vocals.wav"

        if not os.path.exists(no_vocals_path) or not os.path.exists(vocals_path):
            convert_mp3_to_wav(no_vocals_path[:-4] + ".mp3", no_vocals_path)
            convert_mp3_to_wav(vocals_path[:-4] + ".mp3", vocals_path)
            
        #the names of blobs that will be uploaded to gcs
        full_audio_blob = bucket.blob("non_split_audio/full-audio/" + audio_filename + ".wav")
        no_vocals_blob = bucket.blob("non_split_audio/instrumental-audio/" + audio_filename + ".wav")
        vocals_blob = bucket.blob("non_split_audio/vocal-audio/" + audio_filename + ".wav")

        #uploading to gcs...    
        full_audio_blob.upload_from_filename(audio_filepath)
        no_vocals_blob.upload_from_filename(no_vocals_path)
        vocals_blob.upload_from_filename(vocals_path)
        
        #removing audios which are already uploaded to gcs
        os.remove(audio_filepath)
        os.remove(no_vocals_path)
        os.remove(vocals_path)
    

def count_audios(directory):
    with os.scandir(directory) as entries:
        return sum(1 for entry in entries if entry.is_file())

def download_blob(bucket, source, destination):
    blob = bucket.blob(source)
    blob.download_to_filename(destination)

def read_data(file_path):
    data_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split("/")
            if len(parts) == 3:
                file_name, start, end = parts
                data_dict[file_name] = (int(start), int(end))
    return data_dict

def find_file_info(data_dict, file_name):
    return data_dict.get(file_name, False)

def split_and_upload_audios():
    storage_client = storage.Client.from_service_account_json('/workspace/ODEUM/react-flask-app/backend/api/odeum-421210-44f51ed247e8.json')
    bucket = storage_client.get_bucket("odeum-musics")

    gcs_non_split_audio_path = "non_split_audio/"
    gcs_split_audio_path = "split_audio/"
    timestampes_path = "timestamps.txt"

    split_info = read_data(timestampes_path)
    
    filenames = [file.name[27:] for file in list(bucket.list_blobs(prefix=gcs_non_split_audio_path+"full-audio/"))]
    for filename in filenames:
        if bucket.blob(gcs_split_audio_path + 'vocal-audio/' + filename).exists():
            continue

        download_blob(bucket, gcs_non_split_audio_path+"full-audio/"+filename, "full_tmp.wav")
        download_blob(bucket, gcs_non_split_audio_path+"instrumental-audio/"+filename, "instr_tmp.wav")
        download_blob(bucket, gcs_non_split_audio_path+"vocal-audio/"+filename, "vocal_tmp.wav")

        start, end = find_file_info(split_info, filename)
        start = int(start * 1000)
        end = int(end * 1000)

        if not start and not end:
            raise Exception("no timestamp info is found in ", filename)

        try:
            full_audio = AudioSegment.from_wav("full_tmp.wav")
            instr_audio = AudioSegment.from_wav("instr_tmp.wav")
            vocal_audio = AudioSegment.from_wav("vocal_tmp.wav")
        except:
            print(f"an error occurred when getting audio {filename}")

        full_audio[start:end].export("full_segment.wav")
        instr_audio[start:end].export("instr_segment.wav")
        vocal_audio[start:end].export("vocal_segment.wav")

        full_split_blob = bucket.blob(gcs_split_audio_path + "full-audio/" + filename)
        instr_split_blob = bucket.blob(gcs_split_audio_path + "instrumental-audio/" + filename)
        vocal_split_blob = bucket.blob(gcs_split_audio_path + "vocal-audio/" + filename)

        full_split_blob.upload_from_filename("full_segment.wav")
        instr_split_blob.upload_from_filename("instr_segment.wav")
        vocal_split_blob.upload_from_filename("vocal_segment.wav")       
        
        os.remove("full_segment.wav")
        os.remove("instr_segment.wav")
        os.remove("vocal_segment.wav")
        os.remove("full_tmp.wav")
        os.remove("instr_tmp.wav")
        os.remove("vocal_tmp.wav")

def upload_mfccs_to_gcs():
    storage_client = storage.Client.from_service_account_json('/workspace/ODEUM/react-flask-app/backend/api/odeum-421210-44f51ed247e8.json')
    bucket = storage_client.get_bucket("odeum-musics")

    gcs_audio_path = "split_audio/"
    gcs_mfcc_dir_path = "mfccs/"
    tmp_filename = "tmp.wav"
    num_segments= 10

    for audio_type in ["full-audio", "instrumental-audio", "vocal-audio"]:
        json_filename = gcs_mfcc_dir_path + audio_type + ".json"
        if bucket.blob(json_filename).exists():
            download_blob(bucket, json_filename, "tmp.json")
            with open("tmp.json", 'r') as file:
                data = json.load(file)
            os.remove("tmp.json")
        else:
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
    filenames = [file.name[27:] for file in list(bucket.list_blobs(prefix="non_split_audio/full-audio/"))]
    
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
        print(mfcc_path)

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
    separate_audios_and_upload()
    split_and_upload_audios()
    upload_mfccs_to_gcs()
    upload_model_output_json_to_gcs()

