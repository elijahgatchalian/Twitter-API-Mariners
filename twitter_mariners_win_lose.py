#   Eli Gatchalian
#   May 4, 2019

import sys
import tkinter as tk
import tweepy
from twitterKeys import CONSUMER_KEY, CONSUMER_KEY_SECRET, ACCESS_KEY, ACCESS_KEY_SECRET
from webbrowser import open_new_tab

#    File has 3 rows in the following order: Tweet ID, Wins, Loses
FILENAME = "seattleMariners.txt"

###    FUNCTIONS   ###
def mariners_won(event):
    global wins
    wins += 1
    wins = str(wins)
    post_tweet_to_thread()
    
def mariners_lost(event):
    global loses
    loses += 1
    loses = str(loses)
    post_tweet_to_thread()
    
def post_tweet_to_thread():
    global tweet_id
    screen_name = api.me()['screen_name']
    new_tweet = api.update_status('@' + screen_name + ' ' + wins + '-' + loses, tweet_id)
    tweet_id = api.get_status(new_tweet['id_str'])['id_str'] #Set tweet_id to newest tweet's id
    open_new_tab("https://twitter.com/" + screen_name + "/status/" + tweet_id)
    update_text_file()

def update_text_file():
    f = open(FILENAME, "w")
    f.writelines(tweet_id + '\n' + wins + '\n' + loses)
    f.close()
    sys.exit() #close everything


#    Authenticating keys from twitterKeys
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_KEY_SECRET)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

#    Initial window set-up
window = tk.Tk()
window.title("Did the Mariners win?")
window.geometry("250x190")

#    Retrieving previous tweet's information
information = open(FILENAME).readlines()
tweet_id = information[0].rstrip()
wins = int(information[1].rstrip())
loses = int(information[2])

#    Adding label on window (W-L)
label = tk.Label(window, text = str(wins) + '-' + str(loses))
label.place(x = 125, y = 25, anchor = 'center')

#    Adding yes/no buttons on window
yes_button = tk.Button(window, text = "Yes")
no_button = tk.Button(window, text = "No")
yes_button.place(x = 100, y = 125, anchor = 'center')
no_button.place(x = 150, y = 125, anchor = 'center')
yes_button.bind("<Button-1>", mariners_won) 
no_button.bind("<Button-1>", mariners_lost)

#    Display window until a button has been clicked.
window.mainloop()
