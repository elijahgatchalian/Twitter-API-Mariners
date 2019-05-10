#   Eli Gatchalian
#   May 6, 2019

import statsapi
from game_status_methods import status_to_method
from datetime import datetime

#   Display all of the team's games today
todays_date = datetime.today().strftime('%m/%d/%Y')
game_day = statsapi.schedule(team=136,start_date=todays_date)

if(bool(game_day)):
    print()
    for game in range(len(game_day)): #Handling Doubleheader days
        game_info = statsapi.get('game', {'gamePk':game_day[game]['game_id'], 'teamId':136})
        run_method = status_to_method.get(game_day[game]['status'])
        if(str(run_method) == 'None'):
            run_method = status_to_method.get('Unknown')
            run_method(game_day[game]['status'])
        else:
            run_method(game_info)
        
        print('\n' + statsapi.linescore(game_info['gamePk']) + '\n') #Display the game's linebox
else:
    team_name = statsapi.get('team', {'teamId':136})['teams'][0]['name']
    print('There is no ' + team_name + ' game today.')
    
