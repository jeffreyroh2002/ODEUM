import sys
import os
import librosa
import json
import math

from pydub import AudioSegment
from datetime import datetime  # Import the datetime module

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

def save_mfcc(n_mfcc=13, n_fft=2048, hop_length=512, num_segments=5):
    dataset_path = "split_audio"
    json_path = "../react-flask-app/backend/api/static/mfccs/tmp"
    os.makedirs(json_path, exist_ok=True)

    for audio_type in ["full-audio", "instrumental-audio", "vocal-audio"]:
        
        audio_path = os.path.join(dataset_path, audio_type)
        data = {
            "mapping": [],
            "mfcc": [],
            "labels": [],
            "filenames": []  # Store the file names
        }

        for file_name in os.listdir(audio_path):
            #loading each file
            file_path = os.path.join(audio_path, file_name)
            signal, sr = librosa.load(file_path, sr=SAMPLE_RATE)

            # calculate the audio file length, and fit the expected_num_mfcc_vectors_per_segment value
            length = int(signal.shape[0]/float(sr))  # measured in seconds for GTZAN Dataset
            print(length)
            num_samples_per_segment = int(SAMPLES_PER_TRACK / num_segments) # here, int(22050 * 30 / 5)

            # need the number of vectors for mfcc extraction to be equal for each segment
            expected_num_mfcc_vectors_per_segment = math.ceil(num_samples_per_segment / hop_length)

            # process segments extracting mfcc and storing data
            for s in range(num_segments):
                start_sample = num_samples_per_segment * s
                finish_sample = start_sample + num_samples_per_segment

                mfcc = librosa.feature.mfcc(y=signal[start_sample:finish_sample],
                                            sr=sr,
                                            n_fft=n_fft,
                                            n_mfcc=n_mfcc,
                                            hop_length=hop_length)
                mfcc = mfcc.T
                # store mfcc for a segment if it has the expected length
                if len(mfcc) == expected_num_mfcc_vectors_per_segment:
                    data["mfcc"].append(mfcc.tolist())  # convert numpy array to list
                    data["labels"].append(0)
                    data["filenames"].append(file_name)  # fixed this line
                    print("{}, segment:{}".format(file_name, s))

            if length != 30 and length == 60 :  # the case that an audio file is 60 secs long
                for s in range(num_segments, num_segments*2):
                    start_sample = num_samples_per_segment * s
                    finish_sample = start_sample + num_samples_per_segment
                    mfcc = librosa.feature.mfcc(y=signal[start_sample:finish_sample],
                                                    sr=sr,
                                                    n_fft=n_fft,
                                                    n_mfcc=n_mfcc,
                                                    hop_length=hop_length)
                    mfcc = mfcc.T

                    # store mfcc for a segment if it has the expected length
                    if len(mfcc) == expected_num_mfcc_vectors_per_segment:
                        data["mfcc"].append(mfcc.tolist())  # convert numpy array to list
                        data["labels"].append(0)
                        data["filenames"].append(file_name)  # fixed this line
                        print("{}, segment:{}".format(file_name, s))
            
            elif length != 30 :
                print(f"Error : {file_name}")

        output_filename = os.path.join(json_path, audio_type + ".json")
        with open(output_filename, "w") as fp:
            json.dump(data, fp, indent=4)


if __name__ == "__main__":
    split_wav_into_segments()
    save_mfcc(num_segments=10)

