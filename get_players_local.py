import json
import csv
import os

print('START')
print('------------------------------'*10)
print()


players = {}

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "data/sheet_raw.csv"
abs_file_path = os.path.join(script_dir, rel_path)
print(abs_file_path)
with open(abs_file_path, "r") as f:
  csv_reader = csv.reader(f)
  players_raw = [x for x in csv_reader]

print(players_raw)

def main(players_raw):
  for player in players_raw[1:]:
    print(player)
    elo = 0
    discord_user = player[1]
    
    if discord_user.lower() in rank_adjust:
      players[discord_user] = rank_adjust[discord_user.lower()]
      continue

    rank = player[3]

    if rank == 'unranked':
      
      if len(player[4]) > 0:
        try:
          level = int(player[4])
        except ValueError:
          # you fuck with me, i fuck with you
          players[discord_user] = 3800
          continue
      else:
        level = 101
      
      if level <= 25:
        elo = 2100
      elif level <= 50:
        elo = 2200
      elif level <= 75:
        elo = 2300
      elif level <= 100:
        elo = 2400
      elif level > 100:
        elo = 2500
      else:
        elo = 2300
    
    elif rank == 'Copper 5':
      elo = 1100
    
    elif rank == 'Copper 4':
      elo = 1200
    
    elif rank == 'Copper 3':
      elo = 1300
    
    elif rank == 'Copper 2':
      elo = 1400
    
    elif rank == 'Copper 1':
      elo = 1500
    
    elif rank == 'Bronze 5':
      elo = 1600
    
    elif rank == 'Bronze 4':
      elo = 1700
    
    elif rank == 'Bronze 3':
      elo = 1800
    
    elif rank == 'Bronze 2':
      elo = 1900
    
    elif rank == 'Bronze 1':
      elo = 2000
    
    elif rank == 'Silver 5':
      elo = 2100
    
    elif rank == 'Silver 4':
      elo = 2200
    
    elif rank == 'Silver 3':
      elo = 2300
    
    elif rank == 'Silver 2':
      elo = 2400
    
    elif rank == 'Silver 1':
      elo = 2500
    
    elif rank == 'Gold 3':
      elo = 2600
    
    elif rank == 'Gold 2':
      elo = 2800
    
    elif rank == 'Gold 1':
      elo = 3000
    
    elif rank == 'Plat 3':
      elo = 3200
    
    elif rank == 'Plat 2':
      elo = 3600
    
    elif rank == 'Plat 1':
      elo = 4000
    
    elif rank == 'Diamond':
      elo = 5000

    players[discord_user] = elo

  return players

players = main(players_raw)
#print(players)

with open('D:\\Documents (D)\\PythonProjects\\10 mans\\players.json', 'w') as f:
  f.write(json.dumps(players)+'\n')



print('FINISHED.')
print(json.dumps(players))