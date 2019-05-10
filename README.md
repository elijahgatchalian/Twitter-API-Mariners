# Twitter-API-Mariners-Post

I'm a huge baseball fan and an even bigger Seattle Mariners fan. In the 2018 season, I started a thread of the team's W-L 
record starting with 162-0 (I can dream). Each loss meant I would add to the tweet with a minus in the win column and a plus 
to the loss column. This 2019 season I changed it up with a thread that started at 0-0, meaning I tweet the results of each game. 162 games means 162 tweets which can get tiresome. This is where I thought to make this process simpler.

For this project I used Twitter's API via tweepy and MLB's API via statsapi. Documentations for both tweepy and statsapi modules: http://docs.tweepy.org/en/latest/ and https://toddrob99.github.io/MLB-StatsAPI/

mariners_game.py: Retrieves all of the team's games today and passes the current status of the game to game_status_methods.py.

game_status_methods.py: Displays different game information depending on the status of the game.

post_mariners_tweet.py: If the game has been completed, game_status_methods.py calls this and attempts to post a tweet if a  
tweet has not already been posted for this game.
