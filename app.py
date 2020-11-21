from flask_cors import CORS
from flask import Flask, render_template, request
from flask import jsonify

import firebase_admin
from firebase_admin import credentials, firestore

import random
from pprint import pprint
import json

cred = credentials.Certificate('./ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()


app = Flask(__name__)

CORS(app)


def update_record(user_name, mood):
    doc_ref = db.collection('users').document(user_name)
    doc_ref.update({'mood': mood})


def suggest_opposite(user_name):
    """ A little broken and untested
    """
    reference = {
        'very_positive': 2,
        'positive': 1,
        'normal': 0,
        'negative': -1,
        'very_negative': -2
    }

    reverse_reference = {value: key for (key, value) in reference.items()}

    doc_ref = db.collection('users').document(user_name)
    doc = doc_ref.get()
    old_mood = reference[doc.to_dict()["mood"]]
    new_mood = -old_mood

    recs = db.collection('users').where(
        'mood', '==', reverse_reference[new_mood])
    # need to check the kind of data it returns
    if not recs or recs is None:
        return "sansyrox"

    obj_dict = random.choice([i for i in recs.get()]
                             ).to_dict()

    rec_name = (obj_dict["additionalInfo"]["screen_name"])
    # .additionalInfo.screen_name)
    print(rec_name)
    return rec_name


def get_tweets(user_name):
    self_tweets, other_tweets = [], []
    doc_ref = db.collection('users').document(user_name)
    doc = doc_ref.get()
    dictionary = doc.to_dict()
    additional_info = dictionary["additionalInfo"]
    for i in dictionary:
        if i == "additionalInfo" or i == "userCategory" or i == "mood":
            continue

        dict_object = dictionary[i]

        if dict_object["is_retweeted"] and dict_object["retweet_author"] != additional_info["screen_name"]:
            other_tweets.append(dict_object)
        else:
            self_tweets.append(dict_object)
    print(other_tweets)


@app.route('/start_analysis', methods=['GET'])
def start_analysis():
    # username as the parameter
    # query the db of the username
    # call the function of ML guys
    return {}


@app.route('/recommend_friends', methods=['GET'])
def w_youtube():
    return {}


@app.route('/seek_motivation', methods=['GET'])
def recommended_songs():
    return {}


if __name__ == "__main__":
    get_tweets("_bruhhmoment_")
    suggest_opposite('_bruhhmoment_')
    app.run(debug=True)
