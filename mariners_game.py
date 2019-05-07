#   Eli Gatchalian
#   May 6, 2019

import sys
import statsapi
from post_mariners_tweet import post_tweet
from datetime import datetime

def todays_games():
    todays_date = datetime.today().strftime('%m/%d/%Y')
    game_day = statsapi.schedule(team=136,start_date=todays_date)
    
    if(bool(game_day)):
        for game in range(len(game_day)): #Handling Doubleheader days
            single_game = game_day[game]
            tweet_game(single_game['game_id'], single_game)
    else:
        print('There is no ' + statsapi.get('team', {'teamId':136})['teams'][0]['name'] + ' game today.')       

def tweet_game(game_id, game_day):
    print(statsapi.linescore(game_id))
    if(game_day['status'] == 'Final' or game_day['status'] == 'Game Over'):
        team_info = statsapi.get('game', {'gamePk':game_id, 'teamId': 136})['gameData']['teams']
        
        if(team_info['away']['id'] == 136):
            record = team_info['away']['record']['leagueRecord']
        else:
            record = team_info['home']['record']['leagueRecord']
            
        results = post_tweet(record['wins'],record['losses'])
        print(results)
        
todays_games()
