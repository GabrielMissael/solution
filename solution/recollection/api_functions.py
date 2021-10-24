import tweepy
from .help_functions import filter_tweet

def search_tweets(api, words, geocode, user_key_names, limit=20, query=None,
					key_names=['text', 'created_at', 'retweet_count', 'favorite_count']):
	tweets = {}
	query  = "%20OR%20".join(words) if not query else query

	c = tweepy.Cursor(
		api.search_tweets,
		q = query,
		tweet_mode = "extended",
		lang = 'es',
		geocode = geocode
	).items()

	while True:
		try:
			if len(tweets) >= limit:
				break
			tweet = c.next()
			tweet_id, tweet_content = filter_tweet(tweet, key_names, user_key_names, words)
			new_tweet = {tweet_id: tweet_content}
			tweets = {**tweets, **new_tweet}
		except StopIteration:
			print('Oooops there is no more!')
			break

	return tweets