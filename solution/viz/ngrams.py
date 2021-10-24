import pandas as pd
import re
import unicodedata
import nltk
from nltk.corpus import stopwords

import plotly.express as px  # Interactive plots
import plotly
import numpy as np
import sys

#Es la unica manera que encontré de hacer que jalara, feel free to change
sys.path.append("/home/zaiddeanda/github/solution/solution/viz/")

from clean_words import clean_words

def ngram(text_dataframe:pd.DataFrame, n, impath):
    #Recibe un texto traducido y limpio
    cleaned_words = clean_words(text_dataframe)

    df = (pd.Series(nltk.ngrams(cleaned_words, n)).value_counts())[:10]

    fig = px.bar(df, orientation='h')
    # Save dataviz
    plotly.offline.plot(fig, filename=impath)
