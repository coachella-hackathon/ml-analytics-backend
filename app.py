from flask_cors import CORS
from flask import Flask
from flask import jsonify

import firebase_admin
from firebase_admin import credentials, firestore

import random

from algorithm import classify, get_recommendations


cred = credentials.Certificate('./ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()


app = Flask(__name__)

CORS(app)


def get_user_mood(user_name):
    doc_ref = db.collection('users').document(user_name)
    doc = doc_ref.get()
    dictionary = doc.to_dict()
    current_mood = dictionary["mood"]
    return current_mood


def update_recommended_friend(user_name, recommendations):
    doc_ref = db.collection('users').document(user_name)
    doc_ref.update({'recommendations': recommendations})


def update_recommended_motivation(user_name, motivation):
    doc_ref = db.collection('users').document(user_name)
    doc_ref.update({'recommendations-motivation': motivation})


def update_record(user_name, mood):
    doc_ref = db.collection('users').document(user_name)
    doc_ref.update({'mood': mood})


def update_tweet_emotion(user_name, happiest_tweet, saddest_tweet):
    doc_ref = db.collection('users').document(user_name)
    doc_ref.update({
        'happiest_tweet': happiest_tweet,
        'saddest_tweet': saddest_tweet,
    })


def suggest_opposite(user_name):
    """ A little broken and untested
    """
    reference = {
        'Cheerful': 2,
        'Satisfied': 1,
        'Depressed': -1,
        'Stressed': -2
    }

    reverse_reference = {value: key for (key, value) in reference.items()}

    doc_ref = db.collection('users').document(user_name)
    doc = doc_ref.get()
    old_mood = reference[doc.to_dict()["mood"]]
    new_mood = -old_mood

    recs = db.collection('users').where(
        'mood', '==', reverse_reference[new_mood])
    # need to check the kind of data it returns
    if not recs or recs is None or not recs.get() or recs.get() is None:
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

        if dict_object is not None and dict_object["is_retweeted"] and dict_object["retweet_author"] != additional_info["screen_name"]:
            other_tweets.append(dict_object)
        else:
            self_tweets.append(dict_object)
    # print(other_tweets)
    return self_tweets, other_tweets


@app.route('/start_analysis/<user_name>', methods=['GET'])
def start_analysis(user_name):
    self_tweets, other_tweets = get_tweets(user_name)
    mood_status, happiest_tweet, saddest_tweet = classify(
        self_tweets, other_tweets)
    update_record(user_name, mood_status)
    update_tweet_emotion(user_name, happiest_tweet, saddest_tweet)
    return jsonify([mood_status, happiest_tweet, saddest_tweet])


@app.route('/recommend_friends/<user_name>', methods=['GET'])
def recommend_friends(user_name):
    recommendations = get_recommendations(get_user_mood(user_name))
    recommendations["friend"] = suggest_opposite(user_name)

    update_recommended_friend(user_name, recommendations)
    return jsonify(recommendations)


if __name__ == "__main__":
    # recommend_friends("WanderingQi")
    app.run()
