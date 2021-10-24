import pandas as pd
import re
import emoji
from googletrans import Translator, constants
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def deEmojify(text):
    return emoji.get_emoji_regexp().sub(r'', text)

def AddSentimentAnalysis(tweet_df_route:str):
    df = pd.read_pickle(tweet_df_route)

    df = df[df['labels'] != -1]

    top_labels = df['labels'].value_counts()[:3].keys().to_list()

    df = df[df['labels'].isin(top_labels)]

    tweets = df['text'].to_list()

    clean_tweets = [re.sub(r'\n', " ", tweet) for tweet in tweets]

    translator = Translator()
    sentiment = SentimentIntensityAnalyzer()

    sentiment_list=[]
    for i, tweet in enumerate(clean_tweets):
        tweet = deEmojify(tweet)
        tweet = translator.translate(tweet, src='es', dest='en').text
        sentiment_dict = sentiment.polarity_scores(tweet)
        sentiment_list.append(sentiment_dict['compound'])

    df['Sentiment'] = sentiment_list

    return df
