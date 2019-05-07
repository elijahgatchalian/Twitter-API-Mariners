#   Eli Gatchalian
#   May 6, 2019

import sys
import statsapi
from post_mariners_tweet import post_tweet
from datetime import datetime

todays_date = datetime.today().strftime('%m/%d/%Y')
game_day = statsapi.schedule(team=136,start_date=todays_date)

if(bool(game_day)):
    game_day = game_day[0]
    game_day_id = game_day['game_id']
else:
    print('There is no ' + statsapi.get('team', {'teamId':136})['teams'][0]['name'] + ' game today.')
    sys.exit()
           
print(statsapi.linescore(game_day_id)) #Display game's linescore

if(game_day['status'] == 'Final'):
    team_info = statsapi.get('game', {'gamePk':game_day_id, 'teamId': 136})['gameData']['teams']
    
    if(team_info['away']['id'] == 136):
        record = team_info['away']['record']['leagueRecord']
    else:
        record = team_info['home']['record']['leagueRecord']
    
    post_tweet(record['wins'],record['losses'])
    
