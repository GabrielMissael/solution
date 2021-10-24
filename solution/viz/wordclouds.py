import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def GenWordcloud(text_dataframe:pd.DataFrame, filename):
    text = " ".join(text_dataframe['text'])
    wordcloud = WordCloud().generate(text)
    wordcloud.to_file(filename)