#   Eli Gatchalian
#   May 6, 2019

from statsapi import get, linescore, schedule
from game_status_methods import status_to_method
from datetime import datetime  

try:
    game_day = schedule(team=136,start_date=datetime.today().strftime('%m/%d/%Y'))
except:
    print('\nError retrieving today\'s game\n')
    exit()
    
print()

if(len(game_day) == 0):
    try:
        status_to_method.get('No Game Today')()
    except Exception as e:
        print('Error with ' + str(status_to_method.get('No Game Today')) + '\n')
        print(e)
else:
    for game in range(len(game_day)): #Handling Doubleheader days
        gamePk = game_day[game]['game_id']
        
        try: #Getting game's information
            game_info = get('game', {'gamePk':gamePk, 'teamId':136})
        except:
            print('Error retrieving gamePk: ' + gamePk)
            continue #Continuing to next game in case of doubleheader game
            
        #Getting method based on game status
        run_method = status_to_method.get(game_day[game]['status']) 
        
        if(str(run_method) == 'None'): 
            run_method = status_to_method.get('Unknown')
            
        try: #Execute method
            run_method(game_info)
        except Exception as e:
            print('Error with ' + str(run_method))
            print(e)
            continue #Continuing to next game in case of doubleheader game
        
        try: #Display the game's linebox
            print('\n' + linescore(gamePk) + '\n')
        except:
            print('Error displaying linescore for gamePk: ' + gamePk)
