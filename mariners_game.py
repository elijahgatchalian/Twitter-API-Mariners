#   Eli Gatchalian
#   May 6, 2019

import statsapi
from post_mariners_tweet import post_tweet
from datetime import datetime

#   Return the team's wins and losses resulting from the game
def team_record(game_info):
    team_info = game_info['gameData']['teams']
    
    if(team_info['away']['id'] == 136):
        record = team_info['away']['record']['leagueRecord']
    else:
        record = team_info['home']['record']['leagueRecord']
        
    return record['wins'], record['losses']

#   Get all of the team's games today and determine if a tweet is ready to be sent out or not
def todays_games():
    todays_date = datetime.today().strftime('%m/%d/%Y')
    game_day = statsapi.schedule(team=136,start_date=todays_date)
    
    if(bool(game_day)):
        for game in range(len(game_day)): #Handling Doubleheader days
            print()
            game_info = statsapi.get('game', {'gamePk':game_day[game]['game_id'], 'teamId':136})
            ballgame(game_info, game_day[game]['status'])
    else:
        team_name = statsapi.get('team', {'teamId': 136})['teams'][0]['name']
        print('There is no ' + team_name + ' game today.')        

#   Show status of the game
def ballgame(game_info, game_status):
    if(game_status in ['Final', 'Game Over']):
        wins, losses = team_record(game_info)
        print(post_tweet(wins, losses))
    elif(game_status != 'Postponed'):
        live_game = game_info['liveData']['linescore']
        inning = live_game['currentInningOrdinal']
        inning_state = live_game['inningState']
        print(inning_state + ' of the ' + inning)
        if(inning_state not in ['Middle', 'End']):
            batter = live_game['offense']['batter']['fullName']
            # Count
            balls = str(live_game['balls'])
            strikes = str(live_game['strikes'])
            outs = str(live_game['outs'])
            print('At bat: ' + batter)
            print(balls + '-' + strikes + ', ' + outs + ' out(s)')
    else:
        print('This game is postponed.')
        
    print('\n' + statsapi.linescore(game_info['gamePk']) + '\n') #Display the game's linebox
        
todays_games()
