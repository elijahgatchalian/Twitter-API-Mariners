#   Eli Gatchalian
#   May 10, 2019

from post_mariners_tweet import post_tweet

#   Game has completed, attempt to post tweet
def after_game(game_info):
    team_info = game_info['gameData']['teams']
    
    if(team_info['away']['id'] == 136):
        record = team_info['away']['record']['leagueRecord']
    else:
        record = team_info['home']['record']['leagueRecord']
    
    print(post_tweet(record['wins'], record['losses']))

#   Game has not started yet
def before_game(game_info):
    time = game_info['gameData']['datetime']
    location = game_info['gameData']['teams']['home']['locationName']
    print('This game is scheduled to start at ' + time['time'] + time['ampm'] + ' in ' + location + '.')

#   Game in progress. Display inning, pitcher, and batter info
def game_in_progress(game_info):
    live_game = game_info['liveData']['linescore']
    inning = live_game['currentInningOrdinal']
    inning_state = live_game['inningState']
    print(inning_state + ' of the ' + inning)
    
    if(inning_state not in ['Middle', 'End']):
        pitcher = live_game['defense']['pitcher']['fullName']
        batter = live_game['offense']['batter']['fullName']
        balls = str(live_game['balls'])
        strikes = str(live_game['strikes'])
        outs = str(live_game['outs'])
        print('Pitcher: ' + pitcher)
        print('At bat: ' + batter)
        print(balls + '-' + strikes + ', ' + outs + ' out(s)')

#   Game has been postponed for any number of reasons
def game_postponed(game_info):
    print('This game has been postponed.')

#   Game has been either delayed for any number of reasons, or something else
def figure_out_status(game_status):
    game_status = game_status.replace(':','').split(' ')
    if(game_status[0] == 'Delayed'):
        print('This game is delayed due to ' + game_status[1].lower() + '.')
    else:
        print('Unknown game status: ' + game_status[0])
  
#   Dictionary where keys are game statuses and values are methods
#   This is used to avoid numerous if/else statements   
status_to_method = {
'Final': after_game,
'Game Over': after_game,
'Scheduled': before_game,
'Pre-Game': before_game,
'In Progress': game_in_progress,
'Postponed': game_postponed,
'Unknown': figure_out_status
}  
  
