#   Eli Gatchalian
#   May 4, 2019

import tweepy
from twitterKeys import CONSUMER_KEY, CONSUMER_KEY_SECRET, ACCESS_KEY, ACCESS_KEY_SECRET
from webbrowser import open_new_tab

FILENAME = "seattleMariners.txt"

#   Authenticate keys from developer.twitter.com
def authenticate_keys():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_KEY_SECRET)
    return tweepy.API(auth, parser=tweepy.parsers.JSONParser())

#   Return True if previous tweet does not match the W-L record we are trying to tweet now.
#   Return False otherwise.
def check_previous_tweet(wins, losses, tweet_id, api):
    prev_tweet = api.get_status(tweet_id)['text']
    prev_tweet = prev_tweet.replace('-', ' ').split(' ')
    return (not(prev_tweet[1] == str(wins) and prev_tweet[2] == str(losses)))

#   Write the new tweet_id to FILENAME
def write_to_file(tweet_id):
    f = open(FILENAME, 'w')
    f.write(tweet_id)
    f.close()

#   Post tweet of the team's record after today's game results.
#   Return the results of posting the tweet.
def post_tweet(wins, losses):
    tweet_id = open(FILENAME).read()
    api = authenticate_keys()
    screen_name = api.me()['screen_name']
    url = 'https://twitter.com/' + screen_name + '/status/'
    
    if(check_previous_tweet(wins,losses,tweet_id,api)):
        new_tweet = api.update_status('@' + screen_name + ' ' + str(wins) + '-' + str(losses), tweet_id)
        tweet_id = new_tweet['id_str'] #Set tweet_id to newest tweet's id
        write_to_file(tweet_id)
        results = 'Tweet successfully posted.'
        open_new_tab(url + tweet_id)
    else:
        results = 'This game was already tweeted.\n' + url + tweet_id
        
    return results
