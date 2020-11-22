# ml-analytics backend

This project was developed for the Twitter global hackathon **Codechella 2020**, as one of the three main repositories. It is based on mainly two parts:

## Flask Server

We have built a Flask Server that hosts the Machine Learning model and provides and API for the following methods:

* `start_analysis`: gets the model to predict the mood status, happiest and saddest tweets of the user with the passed user_name, updating the records in DB when finished
* `recomend_friends`: given a user_name, this method builds personalized recommendations based on his/her mood status. This recommendations are based on:
  * *big_accounts*: accounts with great number of followers that could improve the self wellness of the user with their content
  * *hashtags*: topics that could help the user with his/her self wellbeing
  * *friends*: possible users to contact. They are selected based on the opposite mood status. For example, if a person is Depressed, we will try to match him/her to a Cheerful person.

## Machine Learning model and Scoring algorithm

Since we want to classify users based on their mood status, we would like to analyze the emotions in their last tweets. Based on this idea, we have focused on building a text emotion classifier:

* *Emotion Classifier*: finding and building this classifier was one of the most challenging tasks the ML team had. Since we did not want to use standard sentiment classifiers that just classified text as positive, neutral and negative; we had to look for more advanced models that could classify a tweet based on the emotions in it. Based on [this notebook](https://www.kaggle.com/praveengovi/classify-emotions-in-text-with-bert), that uses `PyTorch`and `Bert` NLP model, we trained ourselves a model using google colab (so as to get access to GPUs) and stored it. You can find the stored model in `model/` directory, and the tokenizer in the `tokenizer/`directory. 

Once we got the trained model, we built the `ClassificationModel`object so as to have better access to generating predictions. With that done, we decided to build a scoring algorithm on top of it:

* *Scoring algorithm*: the built model returns a likelihood score per emotion and tweet. So as to take into account the different importance each tweet has, we apply a scoring based on the following variables:
  * *n_days*: how old is the tweet? We would like more recent tweets to have extra value
  * *activity*: has the tweet generated lots of impressions? We would like important tweets to have extra value
  * *owner*: is the user that we are analyzing the author of the tweet? We would like owned tweets to have extra value

In order to select the user's mood status, we compute the mean of the scores for each emotion. After that, we check if positivity or negativity is greater, so as to assign a positive or negative mood status. After that, users with more fear and sadness are classified as Depressed, while users with more anger are classified as Stressed. For the positive branch, if we detect there is a lot of positivity in their profile, we set that user as Cheerful, and if not, Satisfied.

## Future Work

* Optimize Emotional Classifier and Scoring algorithm taking sarcasm and other factors into account
* Re-train model with larger dataset (due to computational limitation, we could only train the model with 3k records)
* Find optimal values for the coefficients involved in the scoring algorithm