import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords

def GenWordcloud(text_dataframe:pd.DataFrame, filename):
   	tweets = text_dataframe['text'].to_list()
	text = [word for tweet in tweets for word in tweet.split(" ")]
	# print(stopwords.words('spanish'))
	text = [ word.lower() for word in text if word.lower() not in stopwords.words('spanish') ]
	text = [ word for word in text if not 'http' in word]
	text = " ".join(text)
	print(len(text))
	print(text[:500])
	wordcloud = WordCloud().generate(text)
	wordcloud.to_file(filename)