from googletrans import Translator, constants
import pandas as pd

translator = Translator()

def TranslateDataframe(text_dataframe:pd.DataFrame):
    #Recibe un texto crudo y lo traduce al inglés
    text_list = text_dataframe['text'].tolist()
    translated_list = []
    for text in text_list:
        translated_list.append(translator.translate(text, src='es', dest='en').text)
    text_dataframe['text'].replace(translated_list, inplace=True)
    return text_dataframe