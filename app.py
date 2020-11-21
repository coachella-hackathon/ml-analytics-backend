from flask_cors import CORS
from flask import Flask, render_template, request
from flask import jsonify

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()


app = Flask(__name__)

CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend_friends', methods=['GET'])
def w_youtube():
    pass


@app.route('/seek_motivation', methods=['GET'])
def recommended_songs():
    return pass
