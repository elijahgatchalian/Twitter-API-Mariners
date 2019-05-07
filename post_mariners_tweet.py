#   Eli Gatchalian
#   May 4, 2019

import sys
import tweepy
from twitterKeys import CONSUMER_KEY, CONSUMER_KEY_SECRET, ACCESS_KEY, ACCESS_KEY_SECRET
from webbrowser import open_new_tab

FILENAME = "seattleMariners.txt"

def authenticate_keys():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_KEY_SECRET)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    return api
    
def write_to_file(tweet_id):
    f = open(FILENAME, 'w')
    f.write(tweet_id)
    f.close()

def post_tweet(wins,losses):
    tweet_id = open(FILENAME).read()
    api = authenticate_keys()
    screen_name = api.me()['screen_name']
    new_tweet = api.update_status('@' + screen_name + ' ' + str(wins) + '-' + str(losses), tweet_id)
    tweet_id = new_tweet['id_str'] #Set tweet_id to newest tweet's id
    write_to_file(tweet_id)
    open_new_tab("https://twitter.com/" + screen_name + "/status/" + tweet_id)
