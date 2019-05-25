#   Eli Gatchalian
#   May 10, 2019

#   Game has completed. Attempt to post tweet and display next game info
def after_game(game_info):
    home_away = 'home' if game_info['gameData']['teams']['home']['id'] == 136 else 'away'
    record = game_info['gameData']['teams'][home_away]['record']['leagueRecord']
        
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
    inning = game_info['liveData']['linescore']['currentInningOrdinal']
    inning_state = game_info['liveData']['linescore']['inningState']
    print(inning_state + ' of the ' + inning)
    
    if(inning_state in ['Top', 'Bottom']):
        pitcher = game_info['liveData']['linescore']['defense']['pitcher']
        batter = game_info['liveData']['linescore']['offense']['batter']
        pitcher_home_away = 'home' if inning_state == 'Top' else 'away'
        batter_home_away = 'home' if pitcher_home_away == 'away' else 'away'
        print('Pitcher: ' + pitcher['fullName'] + ', ERA: ' + pitcher_era(pitcher_home_away, str(pitcher['id']), game_info['liveData']['boxscore']['teams']))
        print('At bat: ' + batter['fullName'] + ', AVG: ' + batting_avg(batter_home_away, str(batter['id']), game_info['liveData']['boxscore']['teams']))
        print(str(game_info['liveData']['linescore']['balls']) + '-' + str(game_info['liveData']['linescore']['strikes']) + ', ' + str(game_info['liveData']['linescore']['outs']) + ' out(s)')

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
        # Sometimes next_game() returns back date of recent game
        return
    
    print('The next game is on ' + next_date + '.\n') 
    game_day = schedule(team=136,start_date=next_date)
    game_info = get('game', {'gamePk':game_day[0]['game_id'], 'teamId':136})
    before_game(game_info) 
  
#   Return pitcher's era
def pitcher_era(home_away, player_id, game):
    return game[home_away]['players']['ID' + player_id]['seasonStats']['pitching']['era']

#   Return batter's batting average
def batting_avg(home_away, player_id, game):
    return game[home_away]['players']['ID' + player_id]['seasonStats']['batting']['avg']
    
