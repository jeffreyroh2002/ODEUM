from flask import render_template, request, Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return jsonify(message="Hello from Flask!")

    