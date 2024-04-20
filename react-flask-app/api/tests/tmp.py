from api import create_app, db

app = create_app()

from ..main import NUM_AUDIO

from ..models import Test, UserAnswer, AudioFile

from datetime import datetime
import os
import json
import random

genre_columns = ['Rock', 'Hip Hop', 'Pop Ballad', 'Electronic', 'Jazz', 'Korean Ballad', 'R&B/Soul']
mood_columns = ['Emotional', 'Tense', 'Bright', 'Relaxed']
vocal_columns = ['Smooth', 'Dreamy', 'Raspy']
columns = genre_columns + mood_columns + vocal_columns

def show_audio_data(audio_id):
    with app.app_context():
        audio_file = db.get_or_404(AudioFile, audio_id)
        dominant_genre = audio_file.genre
        print(dominant_genre['R&B/Soul'])

def search_audio_using_attributes(attribute):
    if attribute in genre_columns:
        attribute_type = "dominant_genre"
    elif attribute in mood_columns:
        attribute_type = "dominant_mood"
    else: attribute_type = "dominant_vocal"

    with app.app_context():
        return AudioFile.query.filter_by(**{attribute_type: attribute}).all()

def choose_representative_musics():
    chosen_music_ids = []

    for column in columns:
        if column != "Pop Ballad":
            searched_musics = search_audio_using_attributes(column)
            searched_musics = [music for music in searched_musics if music.id not in chosen_music_ids]
            sample_musics = random.sample(searched_musics, 1)
            chosen_music_ids.extend(sample_music.id for sample_music in sample_musics)

    return chosen_music_ids



def get_next_audio_for_type_1(test_id):
    with app.app_context():
        #get existing test data
        test = Test.query.get_or_404(test_id)

        #getting answered audio ids in the current test
        answers = UserAnswer.query.filter_by(test_id=test_id).all()
        
        #the case when the test is over
        if len(answers) >= 30: return 0

        answered_audios_id = []
        answered_audios_id.extend(answer.audio_id for answer in answers)
        print("answered audio id: ", answered_audios_id)

        #getting test progress (one of "searching genre preference", "analyzing genre preference", "analyzing additional preference")
        test_progress = test.progress    

        previous_answer = UserAnswer.query.filter_by(test_id=test_id) \
                                          .order_by(UserAnswer.question_index.desc()).first()

        #first, we search the user's searching genre preference
        if test_progress == "searching genre preference":
            #randomly iterate each genre and choose one audio that contains the genre dominantly
            answered_genres = []
            answered_genres.extend(answer.dominant_genre for answer in answers)
            unanswered_genres = [genre for genre in genre_columns if genre not in answered_genres]
            print("answered: ", answered_genres, "unanswered: ", unanswered_genres)

            # 1. when the genre preference searching is in progress
            if unanswered_genres:
                #the case when the user rated the previous answer positively
                if previous_answer and previous_answer.overall_rating >= 2:
                    test.progress = "analyzing genre preference"
                
                #the case when the user didn't rate it highly 
                else:
                    next_genre = random.choice(unanswered_genres)
                    possible_audios = search_audio_using_attributes(next_genre, answered_audios_id)
                    if not possible_audios:
                        raise NoMatchingAudioError(f'No matching audios in question index {question_index} and progress {test.progress}')
                    next_audio = random.choice(possible_audios)
                    next_audio_id = next_audio.id

            # 2. when there is no genre preference 
            else:
                genre_rating = {'Rock': 0, 'Hip Hop': 0, 'Pop Ballad': 0, 'Electronic': 0, 'Jazz': 0, 'Korean Ballad': 0, 'R&B/Soul': 0}
                for answer in answers:
                    audio_genre = AudioFile.query.get_or_404(answer.audio_id).genre
                    for genre, value in genre_rating.items():
                        genre_rating[genre] += value
                
                preferred_genre = max(genre_rating, key=genre_rating.get)
                possible_audios = search_audio_using_attributes(preferred_genre, answered_audios_id)
                if not possible_audios:
                    raise NoMatchingAudioError(f'No matching audios in question index {question_index} and progress {test.progress}')
                next_audio = random.choice(possible_audios)
                next_audio_id = next_audio.id
                test.progress = "analyzing genre preference"

        if test_progress == "analyzing genre preference":
            if len(answers) >= 9:
                test.progress = "analyzing additional preference"
            else:
                previous_audio_genre = AudioFile.query.get_or_404(previous_answer.audio_id).dominant_genre
                possible_audios = search_audio_using_attributes(previous_audio_genre, answered_audios_id)
                if not possible_audios:
                    raise NoMatchingAudioError(f'No matching audios in question index {question_index} and progress {test.progress}')
                next_audio = random.choice(possible_audios)
                next_audio_id = next_audio.ids

        else:
            if previous_answer.rating >= 2:
                next_criteria = random.choice(["dominant_genre", "dominant_mood", "dominant_vocal"])
                previous_answer_attribute = getattr(previous_answer, next_criteria)
                possible_audios = search_audio_using_attributes(previous_answer_attribute, answered_audios_id)
                if not possible_audios:
                    raise NoMatchingAudioError(f'No matching audios in question index {question_index} and progress {test.progress}')
                next_audio = random.choice(possible_audios)
                next_audio_id = next_audio.id            

            else:
                disparate_audios = AudioFile.query.filter(
                    dominant_genre != previous_answer.dominant_genre,
                    dominant_mood != previous_answer.dominant_mood,
                    dominant_vocal != previous_answer.dominant_vocal,
                )
                if not disparate_audios:
                    raise NoMatchingAudioError(f'No matching audios in question index {question_index} and progress {test.progress}')
                non_overlapping_disparate_audios = []
                non_overlapping_disparate_audios.extend(audio for audio in disparate_audios if audio not in answered_audios_id)
                next_audio = random.choice(non_overlapping_disparate_audios)
                next_audio_id = next_audio.id

        db.session.commit()
        return next_audio_id
                    
            
            
def show_audio_data(audio_id):
    with app.app_context():
        audio_file = db.get_or_404(AudioFile, audio_id)
        dominant_genre = audio_file.genre
        print(dominant_genre['R&B/Soul'])

def search_audio_using_attributes(attribute, answered_audios_id):
    if attribute in genre_columns:
        attribute_type = "dominant_genre"
    elif attribute in mood_columns:
        attribute_type = "dominant_mood"
    else: attribute_type = "dominant_vocal"

    with app.app_context():
        searched_answers = AudioFile.query.filter_by(**{attribute_type: attribute}).all()
        non_overlapping_answers = []
        non_overlapping_answers.extend(answer for answer in answers if answer.id not in answered_audios_id)

        return non_overlapping_answers

def choose_representative_musics():
    chosen_music_ids = []

    for column in columns:
        if column != "Pop Ballad":
            searched_musics = search_audio_using_attributes(column)
            searched_musics = [music for music in searched_musics if music.id not in chosen_music_ids]
            sample_musics = random.sample(searched_musics, 1)
            chosen_music_ids.extend(sample_music.id for sample_music in sample_musics)

    return chosen_music_ids

class NoMatchingAudioError(Exception):
    pass