import json
import random
from datetime import datetime
from classification_model import ClassificationModel

DAYS_COEF = 10
ACTIVITY_COEF = 7
OWNER_COEF = 0.75
POSITIVITY_COEF = 1.5


def __get_tweet_text(tweets: list) -> list:
    """
    :param tweets: list of dictionaries with tweet info
    :return: list with the tweet text for every item
    """
    return [tweet['tweet_text'] for tweet in tweets]


def apply_scoring(tweet_emotions: list, n_days: int, activity: int, owner_coef: float):
    """
    Apply transformation of each emotion (0-1 value) to take into account
    factors like number of days since tweet, how much activity the tweet generated
    and if the current user is the owner or not of that tweet
    :param tweet_emotions: list of emotions
    :param n_days: days since tweet was published + 1 (to avoid division by zero)
    :param activity: int representing activity (retweets, likes, ...)
    :param owner_coef: coef to apply if owner is current user
    """
    for i in range(len(tweet_emotions)):
        tweet_emotions[i] = (owner_coef * (DAYS_COEF / n_days) * (ACTIVITY_COEF * activity)) * tweet_emotions[i]


def update_scoring(tweets: list, emotions: list, owned_by_user: bool):
    """
    Update the scoring of emotions based on tweet data
    :param tweets: list of tweets
    :param emotions: list of lists containing emotions per tweet
    :param owned_by_user: True if current user is the owner of all tweets
    """
    owner_coef = OWNER_COEF if owned_by_user else (1 - OWNER_COEF)
    for tweet, tweet_emotions in zip(tweets, emotions):
        delta = datetime.now() - datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        # n_days = days since tweet was posted + 1 (to avoid division by zero)
        n_days = delta.days + 1
        activity = tweet['like_count'] + tweet['retweet_count']
        apply_scoring(tweet_emotions, n_days, activity, owner_coef)


def classify(self_tweets: list, other_tweets: list) -> str:
    """
    Classification function to determine mood status based on
    Twitter activity of a user
    :param self_tweets: tweets owned by current user
    :param other_tweets: tweets not owned by current user
    :return: mood_status
    """
    model = ClassificationModel()
    emotions_transformed = []
    for tweets, owned_by_user in ((self_tweets, True), (other_tweets, False)):
        emotions = model.predict_emotions(__get_tweet_text(tweets))
        update_scoring(tweets, emotions, owned_by_user)
        emotions_transformed += emotions
    final_scores = list(map(lambda l: sum(l) / len(l),
                            zip(*emotions_transformed)))
    anger, fear, joy, love, sadness, surprise = final_scores
    positivity = joy + love + surprise
    negativity = anger + fear + sadness

    # if mean of negative emotions is greater than positive ones
    if negativity > positivity:
        if anger * 2 > fear + sadness:
            return "Stressed"
        else:
            return "Depressed"
    else:
        if positivity >= POSITIVITY_COEF * negativity:
            return "Cheerful"
        else:
            return "Satisfied"


def get_recommendations(mood_status: str) -> dict:
    """
    :param mood_status:
    :return: personalized recommendations (big_accounts, hashtags)
    """
    with open("recommendations.json") as json_f:
        try:
            recommendations = json.load(json_f)[mood_status]
        except KeyError:
            raise ValueError(f"Mood status {mood_status} not supported")
    return {"big_accounts": random.sample(recommendations["big_accounts"], 3),
            "hashtags": random.sample(recommendations["hashtags"], 3)}


if __name__ == '__main__':
    classify(["This looks amazing!", "Im so sad..."], ["This looks amazing!", "Im so sad..."])
