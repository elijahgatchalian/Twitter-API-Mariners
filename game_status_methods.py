#   Eli Gatchalian
#   May 10, 2019

#   Game has completed. Attempt to post tweet and display next game info
def after_game(game_info):
    team_info = game_info['gameData']['teams']
    
    if(team_info['away']['id'] == 136):
        record = team_info['away']['record']['leagueRecord']
    else:
        record = team_info['home']['record']['leagueRecord']
    
    from post_mariners_tweet import post_tweet
    post_tweet(record['wins'], record['losses'])
    get_next_game()

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

#   No game today. Display the date of the next game
def no_game():
    print('There is no game today.\n')
    get_next_game()
    print()
    
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
'Warmup': before_game,
'In Progress': game_in_progress,
'Postponed': game_postponed,
'No Game Today': no_game,
'Unknown': figure_out_status
}  
  
#   Display the date of the team's next game
def get_next_game():
    from statsapi import get, next_game, schedule
    from datetime import datetime
    next_date = get('game', {'gamePk': str(next_game(136))})['gameData']['datetime']['originalDate']
    next_date = datetime.strptime(next_date, '%Y-%m-%d').strftime('%m/%d/%Y')
    
    if(next_date == datetime.today().strftime('%m/%d/%Y')):
        # I believe there is a bug with next_game. It seems if the game is in Game Over
        # status, the next_game returns that game. It isn't until the game is in
        # Final status that the next_game actually returns the next game.
        return
    
    print('The next game is on ' + next_date + '.\n') 
    game_day = schedule(team=136,start_date=next_date)
    game_info = get('game', {'gamePk':game_day[0]['game_id'], 'teamId':136})
    before_game(game_info) 
    
