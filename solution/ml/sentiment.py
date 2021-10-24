import pandas as pd
import re
import emoji
from googletrans import Translator, constants
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def deEmojify(text):
    return emoji.get_emoji_regexp().sub(r'', text)

def AddSentimentAnalysis(tweet_df_route:str):
    df = pd.DataFrame(tweet_df_route)

    df = df[df['labels'] != -1]

    tweets_count = df['labels'].value_counts()
    top_labels = [x[0] for x in tweets_count.items() if x[1] > 50]

    df = df[df['labels'].isin(top_labels)]
    df.head(2)

    tweets = df['text'].to_list()

    clean_tweets = [re.sub(r'\n', " ", tweet) for tweet in tweets]

    translator = Translator()
    sentiment = SentimentIntensityAnalyzer()

    sentiment_list=[]
    for i, tweet in enumerate(clean_tweets):
        tweet = deEmojify(tweet)
        sentiment_dict = sentiment.polarity_scores(tweet)
        sentiment_list.append(sentiment_dict['compound'])
    df['Sentiment'] = sentiment_list

    return df
