from .config import twitter_config
from .api_functions import  search_tweets
from .help_functions import create_json_file, percent_encoding
import os

def pipeline(key, words, limit = 4000):

	# Create query
	words = [percent_encoding(x) for x in words.split(', ')]

	# Set up our api
	twitter_api = twitter_config()

	# Define specifcs
	key_names = [
		'text',
		'full_text',
		'created_at',
		'retweet_count',
		'favorite_count',
		'user',
	]
	user_key_names = [
		'location',
	]
	geocodes = {
		"spain": "40.34866,-3.61702,779.11km",
		"mexico": "23.93537,-102.57635,1881km",
		"peru": "-9.19156,-74.39181,1124km",
		"argentina": "-35.44682,-65.17536,1669km",
		"colombia": "3.92721,-73.07773,723.46km",
		#"venezuela": "10.16213,-66.16383,834km",
	}

	# Search tweets with specifics for each country
	for country in geocodes:
		print(f"Extracting from {country}...")
		tweets = search_tweets(
			twitter_api,
			words = words,
			geocode = geocodes[country],
			limit = limit,
			key_names = key_names,
			user_key_names = user_key_names
		)

		if not os.path.exists(f'./data/{country}/{key}'):
  			os.makedirs(f'./data/{country}/{key}')

		# Create json file
		file = f'./data/{country}/{key}/tweets.json'

		create_json_file(tweets, file)

		# Print the total
		print(len(tweets), ' Tweets collected')
		print("-------------------------------")

def get_tweets(n = 4000):

	# Define key words for query search
    words = {
        'salud_financiera': 'ahorro, dinero, "tarjeta de crédito", hipoteca, sueldo, salario',

        'futuro_sostenible': 'contaminación, cambio climático, calentamiento global, sostenible, ecológico',

        'excelencia_operativa': 'BBVA, Bancomer',
    }

    banks = {
        'México': 'Banorte, Citibanamex, Santander, HSBC, Scotiabank',

        'Colombia': 'Bancolombia, "Banco de Bogotá", Davivienda, Banco W',

        'España': 'Santander, CaixaBank, Bankia, "Banco de Sabadell", Bankinter',

        'Perú': '"Banco de crédito del Perú", Scotiabank, Interbank, "Banco Falabella", "Banco de comercio"',

        'Argentina': '"Banco de la nación argentina", "Banco de la provincia de Buenos Aires", Santander, "Banco de Galicia y Buenos Aires", "Banco Macro"',
    }

    for key in words:
        print('--------------------------------')
        print(f'Getting tweets for {key}: ')
        pipeline(key, words[key], limit = n)

if __name__ == "__main__":
	get_tweets()