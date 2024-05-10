from flask import Flask, Blueprint, request, redirect, session, url_for, current_app, jsonify
from api import db, login_manager
from api.models import User, AudioFile, UserAnswer, Test
import requests
import os
import base64
import json
from flask_login import login_required, current_user

from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

openai = Blueprint('openai', __name__)

@openai.route("/query_open_ai", methods= ['GET'])
def query_open_ai():

    user = current_user
    

    liked_genre
    liked_artists
    genre_info
    mood_info
    vocal_info 
    llm = ChatOpenAI(openai_api_key="my-api-key", temperature=0, model_name='gpt-3.5-turbo')
    
    my_question= ""
    ai_response = (llm([HumanMessage(content=my_question)]))
    print(ai_response)

    return jsonify({'open_ai_response': ai_response})

'''test cURL
curl -XPOST localhost:5000/query_open_ai
'''