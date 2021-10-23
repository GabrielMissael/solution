import json


def print_methods(obj):
    """
    Prints a list of methods and attribbutes of an object
    not including the built-in methods 

    Args:
            obj (object): Object we want to know methods
    """
    # Loop through methods and attributes and ignore the ones starting with '__'
    for method in dir(obj):
        if not method.startswith('__'):
            print(method)
    print('----------')


def filter_tweet(tweet, key_names, user_key_names, retweets=False):
    tweet = tweet._json

    # Check if contains BBVA in the text
    original_tweet = tweet
    original_id = tweet['id']
    # Check if it is retweeted
    if 'retweeted_status' in tweet and not retweets:
        original_tweet = tweet['retweeted_status']
        original_id = original_tweet['id']
        filtered_tweet = {key: value for key, value in original_tweet.items(
        ) if key in key_names or not key_names}
    # Check if is quoted
    elif 'quoted_status' in tweet and not retweets:
        original_tweet = tweet['quoted_status']
        original_id = original_tweet['id']
        filtered_tweet = {key: value for key, value in original_tweet.items(
        ) if key in key_names or not key_names}
    else:
        filtered_tweet = {key: value for key, value in tweet.items(
        ) if key in key_names or not key_names}

    if 'full_text' in filtered_tweet:
        filtered_tweet['text'] = filtered_tweet.pop('full_text')

    # Formatting user info
    if 'user' in key_names:
        for user_key in user_key_names:
            filtered_tweet[user_key] = filtered_tweet['user'][user_key]

    filtered_tweet.pop('user')

    # Return the filtered tweet
    return original_id, filtered_tweet


def create_json_file(data, file):
    """
    Simply create a json file from a dictionary

    Args:
            data (dict): The data we want to put into the file
            file (str): File location, it has to exist before run this function
    """
    # Open and write the data in a json format
    with open(file, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data, ensure_ascii=False, indent=4))
