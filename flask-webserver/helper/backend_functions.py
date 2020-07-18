import os.path as path
from pathlib import Path
import csv
from datetime import datetime
import platform

filepath = str(Path(__file__).parents[2])+'/data/'

def player_to_csv(player_entry):
  global filepath
  now = datetime.now()
  
  if platform.system() == 'Windows':
    timestamp = now.strftime("%m/%d/%Y %T")
  else:
    timestamp = now.strftime("%m/%d/%Y %H:%M:%S")
  
  discord = player_entry['discord']
  uplay = player_entry['uplay']
  rank = player_entry['rank']
  level = player_entry['level']
  with open(path.join(filepath, 'sheet_raw.csv'), 'a+', newline='') as f:
    # Create a writer object from csv module
    csv_writer = csv.writer(f)
    # Add contents of list as last row in the csv file
    csv_writer.writerow([timestamp, discord, uplay, rank, level])

def clear_csv():
  global filepath
  with open(f'{filepath}sheet_raw.csv', 'r') as f:
    csv_reader = list(csv.reader(f))
    
  csv_header = csv_reader[0]
  with open('sheet_raw.csv', 'w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(csv_header)




