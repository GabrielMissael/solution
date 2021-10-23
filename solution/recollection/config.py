from decouple import config
import tweepy


def twitter_config():
    """
    Set up the tweepy API, the environment variables and authenticate our

    Returns:
            api object: An object that contains all the twitter api functionality
    """
    # Environment variables
    consumer_key = config('TWITTER_API_KEY')
    consumer_secret = config('TWITTER_KEY_SECRET')
    access_token = config('TWITTER_ACCESS_TOKEN')
    access_token_secret = config('TWITTER_ACCESS_TOKEN_SECRET')

    # Authorize API and Get the access token
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Return the api object
    return tweepy.API(auth, wait_on_rate_limit=True)
