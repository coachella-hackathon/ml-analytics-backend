from pprint import pprint
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


def get_tweets(user_name):
    self_tweets, other_tweets = [], []
    doc_ref = db.collection('users').document(user_name)
    doc = doc_ref.get()
    dictionary = doc.to_dict()
    additional_info = dictionary["additionalInfo"]
    for i in dictionary:
        if i == "additionalInfo" or i == "userCategory":
            continue

        dict_object = dictionary[i]
        if dict_object["is_retweeted"] and dict_object["retweet_author"] != additional_info["screen_name"]:
            other_tweets.append(dict_object)
        else:
            self_tweets.append(dict_object)
    print(other_tweets)


@app.route('/recommend_friends', methods=['GET'])
def w_youtube():
    return {}


@app.route('/seek_motivation', methods=['GET'])
def recommended_songs():
    return {}


if __name__ == "__main__":
    get_tweets("_bruhhmoment_")
