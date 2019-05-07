# Twitter-API-Mariners-Post

I'm a huge baseball fan and an even bigger Seattle Mariners fan. In the 2018 season, I started a thread of the team's W-L 
record starting with 162-0 (I can dream). Each loss meant I would add to the tweet with a minus in the win column and a plus 
to the loss column. This season I changed it up with a thread that started at 0-0, meaning I tweet the results of each game. 
162 games means 162 tweets which can get tiresome. This is where I thought to make this process simpler.

For this project I used Twitter's API via tweepy and MLB's API via statsapi. Documentations for both tweepy and statsapi modules: http://docs.tweepy.org/en/latest/ and https://toddrob99.github.io/MLB-StatsAPI/

Here are the steps my program takes:
  1. Check that there is a game today using statsapi.
  2. If there is no game, print out there is no game and exit program immediately. Otherwise, display the game's linescore.
  3. If today's game is over, get the team's current record and post the record to my twitter account using tweepy.
