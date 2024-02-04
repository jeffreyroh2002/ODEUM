import sys
import os
from pydub import AudioSegment
from datetime import datetime  # Import the datetime module

def split_wav_into_segments(input_directory, output_directory, txt_file, segment_length_ms=30000):
    os.makedirs(output_directory, exist_ok=True)

    with open(txt_file, "r") as file:
        content = file.readline()
        count = 1  # Initialize a counter for unique file names
        while content != "":
            content = content.strip()
            data = content.split(",")
            song_name = data[0]
            start_time = int(data[1]) * 1000
            end_time = int(data[2]) * 1000

            input_path = os.path.join(input_directory, song_name)
            audio = AudioSegment.from_wav(input_path)
            segment = audio[start_time:end_time]

            # Generate a unique output file name using a counter or timestamp
            output_file = os.path.join(output_directory, f"{song_name}_{count}.wav")
            # Alternatively, you can use a timestamp for uniqueness:
            # timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            # output_file = os.path.join(output_directory, f"{song_name}_{timestamp}.wav")

            segment.export(output_file, format="wav")
            
            count += 1  # Increment the counter
            content = file.readline()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py input_directory output_directory")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    txt_file_path = sys.argv[3]

    split_wav_into_segments(input_directory, output_directory, txt_file_path)