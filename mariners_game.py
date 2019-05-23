#   Eli Gatchalian
#   May 6, 2019

from statsapi import get, linescore, schedule
from game_status_methods import status_to_method
from datetime import datetime  

#   Display all of the team's games today
todays_date = datetime.today().strftime('%m/%d/%Y')
game_day = statsapi.schedule(team=136,start_date=todays_date)

print()

num_games = len(game_day)

if(num_games == 0):
    status_to_method.get('No Game Today')()
else:
    for game in range(num_games): #Handling Doubleheader days
        game_info = statsapi.get('game', {'gamePk':game_day[game]['game_id'], 'teamId':136})
        run_method = status_to_method.get(game_day[game]['status'])
        
        if(str(run_method) == 'None'):
            status_to_method.get('Unknown')(game_day[game]['status'])
        else:
            run_method(game_info)
        
        print('\n' + statsapi.linescore(game_info['gamePk']) + '\n') #Display the game's linebox
