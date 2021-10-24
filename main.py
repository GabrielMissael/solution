from solution.recollection.get_tweets import get_tweets

from solution.ml.sentiment import AddSentimentAnalysis
from solution.ml.clustering import cluster

from solution.viz.wordclouds import GenWordcloud
from solution.viz.ngrams import ngram
from solution.viz.visualization import scatter

import pandas as pd
import os.path

def process(pais, prioridad):
    file = f'data/{pais}/{prioridad}/embs.pkl'

    if not os.path.exists(file):

        df = cluster(
            file = f'data/{pais}/{prioridad}/tweets.json',
            verbose=True
        )
        df.to_pickle(file)

        df = AddSentimentAnalysis(file)
        df.to_pickle(f'data/{pais}/{prioridad}/sentiment.pkl')

def main():
    # Uncomment if data not available
    # get_tweets(n = 5000)

    paises = ['mexico']
    prioridades = ['excelencia_operativa']

    # Uncomment to run all the 20 dataset (countries and priorities)
    # paises = ['argentina', 'colombia', 'mexico', 'peru', 'spain']
    # prioridades = ['crecimiento', 'excelencia_operativa','futuro_sostenible', 'salud_financiera']

    for pais in paises:
        for prioridad in prioridades:
            process(pais, prioridad)
            path = f'data/{pais}/{prioridad}/'
            print('HEY')
            df = pd.read_pickle(path + 'embs.pkl')

            GenWordcloud(df, path + 'wordcloud.png')

            ngram(df, 2, path + 'ngram.html')

            scatter(df, path + 'scatter.html')

            df = pd.read_pickle(path + 'sentiment.pkl')

if __name__ == '__main__':
    print('HEY')
    main()