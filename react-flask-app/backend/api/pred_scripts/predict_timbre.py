import json
import numpy as np
from tensorflow import keras
import os

# Load the saved model
saved_model_path = os.path.join(
    os.getcwd(), "api", "mlModels", "pred_vocal", "saved_model"
)
test_data_path = "genre_testing_data.json"
mfcc_labels = np.array(["Smooth", "Dreamy", "Raspy", "Voiceless"])


def load_testing_data(test_data_path):
    with open(test_data_path, "r") as fp:
        test_data = json.load(fp)

    X_test = np.array(test_data["mfcc"])  # Adjust the key as per your data format
    y_test = np.array(test_data["labels"])  # Adjust the key as per your data format
    filenames = test_data["filenames"]

    return X_test, y_test, filenames


"""
def load_mfcc_labels(model_saved_mfcc):  # change using txt
    with open(model_saved_mfcc, "r") as fp:
        data = json.load(fp)

    mfcc_labels = np.array(data["mapping"])  # Adjust the key as per your data format

    return mfcc_labels
"""


def predict_timbre(saved_model_path, test_data_path):
    X_test, y_test, filenames = load_testing_data(test_data_path)
    X_test = X_test[..., np.newaxis]  # If needed, reshape your data for the model input

    loaded_model = keras.models.load_model(saved_model_path)

    # Make predictions
    predictions = loaded_model.predict(X_test)

    # If you have a classification task, you can get the predicted class indices:
    predicted_class_indices = np.argmax(predictions, axis=1)

    # Define your label list mapping class indices to labels
    label_list = {}
    for i in range(len(mfcc_labels)):
        label_list[i] = mfcc_labels[i]

    Song_list = set(filenames)
    Song_list = list(Song_list)
    Sorted_Song_list = sorted(Song_list)
    Song_list = {label: [] for label in Sorted_Song_list}

    # sort labels
    for i, label in enumerate(predicted_class_indices):
        f_name = filenames[i]
        Song_list[f_name].append(i)

    # Initialize variables for percentage calculation
    segment_count = 0
    label_counts = {label: 0 for label in label_list.values()}

    output = {}

    for f in Sorted_Song_list:
        predicted_idx = Song_list[f]

        for idx in predicted_idx:
            label = label_list[predicted_class_indices[idx]]

            # Update label counts for percentage calculation
            label_counts[label] += 1
            segment_count += 1

        # Calculate the average radar values for the song
        predicted_timbre = {
            timbre: round(float(percent) / segment_count, 2) for timbre, percent in label_counts.items()
        }

        output[f] = predicted_timbre
        segment_count = 0
        label_counts = {label: 0 for label in label_list.values()}

    return output