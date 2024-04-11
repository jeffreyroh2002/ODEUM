# For easy maintenance

If you want to change the info(number, filename, audio data) of audios or questions, 
modify '/workspace/ODEUM/react-flask-app/api/static'(only for audios)
and change api/main/__init__.py

currently, metadata is 

NUM_AUDIO = 22

NUM_QUESTIONS_PER_AUDIO = 4

NUM_EXTRA_QUESTIONS = 0

EXTRA_QUESTIONS_INDEX = []

NUM_QUESTIONS = NUM_AUDIO * NUM_QUESTIONS_PER_AUDIO + NUM_EXTRA_QUESTIONS

QUESTION_TYPES = ['vocal_timbre_rating', 'overall_rating', 'genre_rating', 'mood_rating']

