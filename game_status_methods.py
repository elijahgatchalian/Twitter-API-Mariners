#   Eli Gatchalian
#   May 10, 2019

#   Game has completed. Attempt to post tweet and get next game information
def after_game(game_info):
    home_away = 'home' if game_info['gameData']['teams']['home']['id'] == 136 else 'away'
    record = game_info['gameData']['teams'][home_away]['record']['leagueRecord']
        
    from post_mariners_tweet import post_tweet
    
    post_tweet(record['wins'], record['losses'])
    
    get_next_game()

#   Game has not started yet
def before_game(game_info):
    time = game_info['gameData']['datetime']
    city = game_info['gameData']['teams']['home']['locationName']
    print('This game is scheduled to start at ' + time['time'] + time['ampm'] + ' in ' + city + '.')

#   Game in progress. Display inning, pitcher, and batter information
def game_in_progress(game_info):
    inning = game_info['liveData']['linescore']['currentInningOrdinal']
    inning_state = game_info['liveData']['linescore']['inningState']
    print(inning_state + ' of the ' + inning)
    
    if(inning_state in ['Top', 'Bottom']):
        print()
        pitcher_home_away = 'home' if inning_state == 'Top' else 'away'
        batter_home_away = 'away' if pitcher_home_away == 'home' else 'home'
        pitcher_info(pitcher_home_away, game_info['liveData'])
        batter_info(batter_home_away, game_info['liveData'])
        count_info(game_info['liveData']['linescore'])
        
#   Game has been postponed for any number of reasons
def game_postponed(game_info):
    print('This game has been postponed.')
    
#   No game today. Get next game information
def no_game():
    print('There is no game today.\n')
    get_next_game()
    print()
    
#   Game has been either delayed or something else
def figure_out_status(game_info):
    game_status = game_info['gameData']['status']['detailedState'].replace(':','').split(' ')
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
    game_day_id = schedule(team=136,start_date=next_date)[0]['game_id']
    game_info = get('game', {'gamePk':game_day_id, 'teamId':136})
    before_game(game_info) 
  
#   Display pitcher information
def pitcher_info(home_away, game):
    pitcher_id = str(game['linescore']['defense']['pitcher']['id'])
    full_name = game['boxscore']['teams'][home_away]['players']['ID' + pitcher_id]['person']['fullName']
    era = game['boxscore']['teams'][home_away]['players']['ID' + pitcher_id]['seasonStats']['pitching']['era']
    pitch_count = str(game['boxscore']['teams'][home_away]['players']['ID' + pitcher_id]['stats']['pitching']['numberOfPitches'])
    print('Pitcher: ' + full_name + ', ERA: ' + era + ', Pitch Count: ' + pitch_count)

#   Display batter information
def batter_info(home_away, game):
    batter_id = str(game['linescore']['offense']['batter']['id'])
    full_name = game['boxscore']['teams'][home_away]['players']['ID' + batter_id]['person']['fullName']
    batting_avg = game['boxscore']['teams'][home_away]['players']['ID' + batter_id]['seasonStats']['batting']['avg']
    at_bats = str(game['boxscore']['teams'][home_away]['players']['ID' + batter_id]['stats']['batting']['atBats'])
    hits = str(game['boxscore']['teams'][home_away]['players']['ID' + batter_id]['stats']['batting']['hits'])
    print('Batter: ' + full_name + ', AVG: ' + batting_avg + ', ' + hits + '-' + at_bats)
    
#   Display count information
def count_info(game):
    balls = str(game['balls'])
    strikes = str(game['strikes'])
    outs = str(game['outs'])
    if(balls == '4' or strikes == '3'):
        print('Count: ' + outs + ' out(s)')
    else:
        print('Count: ' + balls + '-' + strikes + ', ' + outs + ' out(s)')
        
