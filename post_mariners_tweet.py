#   Eli Gatchalian
#   May 4, 2019

FILENAME = "seattleMariners.txt"

#   Authenticate keys from developer.twitter.com
def authenticate_keys():
    from twitterKeys import CONSUMER_KEY, CONSUMER_KEY_SECRET, ACCESS_KEY, ACCESS_KEY_SECRET
    from tweepy import OAuthHandler, API, parsers
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_KEY_SECRET)
    return API(auth, parser=parsers.JSONParser())

#   Return True if previous tweet does not match the W-L record we are trying to tweet now.
#   Return False otherwise.
def check_previous_tweet(wins, losses, tweet_id, api, screen_name):
    prev_tweet = api.get_status(tweet_id)['text']
    prev_tweet = prev_tweet.replace('-', ' ').split(' ')
    size = len(prev_tweet) - 1
    return prev_tweet[size - 1] != str(wins) or prev_tweet[size] != str(losses)
            
#   Write the new tweet_id to FILENAME
def write_to_file(tweet_id):
    f = open(FILENAME, 'w')
    f.write(tweet_id)
    f.close()

#   Post tweet of the team's record after today's game results.
#   Print the results of posting the tweet.
def post_tweet(wins, losses):
    tweet_id = open(FILENAME).read()
    api = authenticate_keys()
    screen_name = api.me()['screen_name']
    url = 'https://twitter.com/' + screen_name + '/status/'
    results = 'This game was already tweeted.\n' + url + tweet_id
    
    if(check_previous_tweet(wins,losses,tweet_id,api,screen_name)):
        from webbrowser import open_new_tab
        new_tweet = api.update_status('@' + screen_name + ' ' + str(wins) + '-' + str(losses), tweet_id)
        tweet_id = new_tweet['id_str'] #Set tweet_id to newest tweet's id
        write_to_file(tweet_id)
        results = 'Tweet successfully posted.'
        open_new_tab(url + tweet_id)
        
    print(results + '\n')
