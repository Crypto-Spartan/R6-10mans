import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import csv

print('STARTING...')
#print()

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('D:\\Documents (D)\\PythonProjects\\10 mans\\conf\\googledata.json', scope)
client = gspread.authorize(creds)
sheet = client.open('10 Man Scrims').sheet1
sheet_raw = sheet.get_all_values()
players_raw = []
players = {}

rank_adjust = {'rex209er':3600, 'j3lly#0666':3700, 'j3lly': 3700, 'fawt.-':3800, 'fawt':3800, 'hybrid':3800}

for i in sheet_raw[1:]:
  i = i[1:]
  players_raw.append(i)
#print(players_raw)

with open("D:\\Documents (D)\\PythonProjects\\10 mans\\data/sheet_raw.csv", "w", newline="") as f:
  writer = csv.writer(f)
  writer.writerows(sheet_raw)

def main():
  for player in players_raw:
    elo = 0
    discord_user = player[0]
    
    if discord_user.lower() in rank_adjust:
      players[discord_user] = rank_adjust[discord_user.lower()]
      continue

    rank = player[2]

    if rank == 'Unranked':
      
      if len(player[3]) > 0:
        try:
          level = int(player[3])
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

main()
#print(players)

with open('D:\\Documents (D)\\PythonProjects\\10 mans\\players.json', 'w') as f:
  f.write(json.dumps(players)+'\n')

print('FINISHED.')
print(json.dumps(players))
