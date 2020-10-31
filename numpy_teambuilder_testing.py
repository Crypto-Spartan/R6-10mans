from itertools import combinations
from tqdm import tqdm
import random
import json
import csv
import sys
import cProfile
import os
import numpy as np


print('START')
print('------------------------------'*10)
print()

players = json.load(open('players.json'))
#print(players)

def get_len(players):
  
  if type(players) is dict:
    length = 0
    for i in players.keys():
      if type(i) is str:
        length += 1
      elif type(i) is tuple:
        length += len(i)
  elif type(players) is list:
    length = 0
    for i in players:
      if type(i) is str:
        length += 1
      elif type(i) is tuple:
        length += len(i)
  else:
    length = len(players)
  return length



def groups_on_same_team(players, groups, full_result_list):
  
  full_result_list_len = len(full_result_list)
  badlist = []
    

  if groups:
    
    for g in groups.keys():
      group_length = len(g)
      
      if group_length == 2:
        for i in range(full_result_list_len):
          r = full_result_list[i]
          if g[0] in r and g[1] not in r:
            badlist.append(r)
          elif g[1] in r and g[0] not in r:
            badlist.append(r)
      
      elif group_length == 3:
        for i in range(full_result_list_len):
          r = full_result_list[i]
          if g[0] in r and (g[1] not in r or g[2] not in r):
            badlist.append(r)
          elif g[1] in r and (g[0] not in r or g[2] not in r):
            badlist.append(r)
          elif g[2] in r and (g[0] not in r or g[1] not in r):
            badlist.append(r)
      
      elif group_length == 4:
        for i in range(full_result_list_len):
          r = full_result_list[i]
          if g[0] in r and (g[1] not in r or g[2] not in r or g[3] not in r):
            badlist.append(r)
          elif g[1] in r and (g[0] not in r or g[2] not in r or g[3] not in r):
            badlist.append(r)
          elif g[2] in r and (g[0] not in r or g[1] not in r or g[3] not in r):
            badlist.append(r)
          elif g[3] in r and (g[0] not in r or g[1] not in r or g[2] not in r):
            badlist.append(r)
      
      elif group_length == 5:
        for i in range(full_result_list_len):
          r = full_result_list[i]
          if g[0] in r and (g[1] not in r or g[2] not in r or g[3] not in r or g[4] not in r):
            badlist.append(r)
          elif g[1] in r and (g[0] not in r or g[2] not in r or g[3] not in r or g[4] not in r):
            badlist.append(r)
          elif g[2] in r and (g[0] not in r or g[1] not in r or g[3] not in r or g[4] not in r):
            badlist.append(r)
          elif g[3] in r and (g[0] not in r or g[1] not in r or g[2] not in r or g[4] not in r):
            badlist.append(r)
          elif g[4] in r and (g[0] not in r or g[1] not in r or g[2] not in r or g[3] not in r):
            badlist.append(r)
    
    badlist_set = {tuple(x.keys()) for x in badlist}
    print('Removing impossible team combos...')
    result_list = [x for x in tqdm(full_result_list) if tuple(x.keys()) not in badlist_set]
    print()
    badlist = []
    badlist_set = set()
    return result_list
  
  else:
    return full_result_list



def lambda_random():
  return lambda k: random.random()

def lambda_sort():
  return lambda x: x[1]



def get_matchups(players):
  total_players = get_len(players)
  top_two = sorted(players.items(), key=lambda x: x[1], reverse=True)[:2]
  #print(top_two)
  players = dict(sorted(players.items(), key=lambda_random()))
  maxruns = total_players // 10
  
  print(f'Players: {total_players}')
  print()
  print(f'PLAYERS TO BE ALLOCATED: {players}')
  print()
  
  groups = get_playergroups(players)
  difference_best = 1
  match_check = 0
  recursive_count = 0
  runtimes = 0
  match = 0
  best_combos = []
  
  full_result_list = [dict(x) for x in combinations(players.items(), 5)]
  player_ids = {k:v for k,v in enumerate(players, 1)}
  id_and_rank = {k:players[v] for k,v in player_ids.items()}
  print(player_ids)
  print(id_and_rank)
  
  full_result_array = np.array([[*[y[0] for y in x], sum([y[1] for y in x])] for x in combinations(id_and_rank.items(), 5)], dtype=object)
  print(full_result_array)
  unique_mmrs, indices, counts = np.unique(full_result_array[:,5], return_inverse=True, return_counts=True)
  print(full_result_array.shape)
  print(unique_mmrs)
  print()
  print(indices)
  print()
  print(counts)
  
  u=set()
  iter_count = 1
  while not u and iter_count < 20:
    iter_count += 1

    mode_idx = list(counts).index(max(counts))
    counts[mode_idx] = 0
    print(mode_idx)
    mode_mmr_team_idx = [i for i, val in enumerate(indices) if val == mode_idx]
    print(mode_mmr_team_idx)
    print()
    teams_w_mode_mmr = full_result_array[mode_mmr_team_idx]
    print(teams_w_mode_mmr)
    print(teams_w_mode_mmr.shape)
    mmr = unique_mmrs[mode_idx]
    teams_to_check = [tuple(x) for x in np.delete(teams_w_mode_mmr, 5, 1)]
    print(teams_to_check)
    team1 = teams_w_mode_mmr[0][:5]
    team2 = teams_w_mode_mmr[-1][:5]  
    print()
    #print(team1)
    #print(team2)
    #print(mmr)
    #print()
    test_arr = [(1, 2, 3, 4, 8),(1, 2, 4, 7, 8),(2, 7, 8, 9, 10),(4, 5, 6, 9, 10),(5, 6, 8, 9, 10),(5, 6, 7, 9, 10)]
    #u = [x for i, x in enumerate(test_arr) if not x - x[i+1]]
    
    for x in teams_to_check:
      for z in teams_to_check:
        if x == z or (x,z) in u:
          continue
        else:
          if not (set(x)) & (set(z)):
            print((set(x)) & (set(z)))
            print(x)
            print(z)
            u.add((x,z))

    if not u:
      print('FAIL')
  
    print(u)
    print('-'*80)

  u = [(tuple(x),tuple(z)) for x,z in u]
  print('DONE')
  print(u)
  sys.exit()

  if groups:
    result_list = groups_on_same_team(players,groups,full_result_list)
  else:
    result_list = full_result_list
  
  result_list_len = len(result_list)
  full_result_list = []

  print(f'Possible Teams: {result_list_len:,}')
  print(f'Possible Combos: {(result_list_len**2) - result_list_len:,}')

  while get_len(players) >= 10:
  
    if runtimes < maxruns:
      runtimes += 1
      difference_best, match_check, recursive_count, best_combos, players = create_match(difference_best, match_check, recursive_count, best_combos, result_list, total_players, players, groups)
    
    elif runtimes < (maxruns + 2):
      runtimes += 1
      difference_best += 100
      difference_best, match_check, recursive_count, best_combos, players = create_match(difference_best, match_check, recursive_count, best_combos, result_list, total_players, players, groups)
    
    else:
      break

    if get_len(players) >= 10 and runtimes < maxruns:
      full_result_list = [dict(x) for x in combinations(players.items(), 5)]
      #full_result_list = list(map(dict, combinations(players.items(), 5)))
      result_list = groups_on_same_team(players,groups,full_result_list)
      full_result_list = []
      result_list_len = len(result_list)
      print(f'Possible Teams Left: {result_list_len:,}')
      print(f'Possible Combos Left: {(result_list_len**2) - result_list_len:,}')

  remaining_player_count = get_len(players)

  print()
  print(f'Matchups Created: {len(best_combos)}')
  print(f'Total Combinations Tried: {recursive_count:,}')
  print()
  
  for matchup in best_combos:
    match += 1
    print(f'MATCH {match} - {matchup[2]} MMR')
    
    if int(matchup[2].split(' ')[1]) > 0:
      print(list(matchup[0]))
      print(list(matchup[1]))
    else:
      print(list(matchup[0])[1:])
      print(list(matchup[1])[1:])
    print()
  
  if remaining_player_count < 10:
    if remaining_player_count > 0:
      print(f'REMAINING PLAYERS ({remaining_player_count}):\n{players}')
      print()
      remaining = list(players.keys())
    
    unbalance_check = 'y'
    
    if unbalance_check[0] == 'y':
      print()
      get_uplay_names(best_combos)
      if remaining_player_count > 0:
        print(f'Players left out: {remaining}')

      return remaining_player_count
    
    else:
      print('\n\n\n')
      print('Matches determined to be uneven, re-running.')
      return 10
  
  else:
    print(f'REMAINING PLAYERS ({remaining_player_count}):\n{players}')
    print('\n\n\n\n')
    print('Couldn\'t find teams, trying again.')
    return remaining_player_count




def create_match(difference_best, match_check, recursive_count, best_combos, result_list, total_players, players, groups):

  for combo in result_list:
    
    if len(best_combos) > match_check:
      match_check += 1
      break

    team1_total = sum(combo.values())
    playerlist = set(combo.keys())  
    
    for teamcheck in result_list[::-1]:
      recursive_count += 1

      if recursive_count % 1000000 == 0:
        print(f'Combinations Tried: {round((recursive_count / 1000000), 2)} Million')

      playerlist_check = list(teamcheck.keys())
      shared_players = [x for x in playerlist_check if x in playerlist]
      
      if not shared_players:
        team2_total = sum(teamcheck.values())
        difference = abs(team1_total - team2_total)
        
        if difference <= difference_best:
          game = []
          difference_best = difference
          combo['total'] = team1_total
          teamcheck['total'] = team2_total
          combo = sorted(combo.items(), key=lambda_sort(), reverse=True)
          teamcheck = sorted(teamcheck.items(), key=lambda_sort(), reverse=True)
          
          if (combo[3][1] > teamcheck[2][1]) or (teamcheck[3][1] > combo[2][1]):
            continue

          game.append(combo)
          game.append(teamcheck)
          game.append(f'difference: {difference}')
                    
          for key in dict(combo).keys():
            if key != 'total':
              del players[key]
          for key in dict(teamcheck).keys():
            if key != 'total':
              del players[key]
            
          best_combos.append(game)
          print(f'Match Created. - Combinations Tried: {recursive_count:,}\n')
          break

  return difference_best, match_check, recursive_count, best_combos, players




def get_playergroups(players):
  groups = {}
    
  #groups_check = input('Did any players signup in a group? (n/no): ').lower() or 'n'
  groups_check = 'n'

  if groups_check[0] == 'y':

    num_of_groups = int(input('How many groups will be formed?: '))
    list_of_groups = []
    
    for num in range(num_of_groups):
      inputted_group = input(f'List members of team/group #{num+1}, separated by a comma: ')
      inputted_group = inputted_group.split(',')
      
      while len(inputted_group) < 2:
        print('Group does not have enough members.')
        inputted_group = input('Enter 0 to quit creating groups, or re-enter group members: ')
      
        if inputted_group == '0':
          return 0
        inputted_group = inputted_group.split(',')
      
      group_list = []
      
      for i in inputted_group:
        i = i.strip()
        
        while i not in players.keys():
          i = input(f'Playername "{i}" not valid. Enter new name: ')
          i = i.strip()
        
        group_list.append(i)
      
      group_list_tuple = tuple(group_list)
      list_of_groups.append(group_list_tuple)

    for g in list_of_groups:
      group_mmr = 0
      
      for p in g:
        group_mmr += players[p]
      
      groups[g] = group_mmr
    
    print()
    print(f'Groups: {groups}')
    print()

  else:
    print('No groups will be formed.')
    print()
  
  return groups




def get_uplay_names(best_combos):
  discord_to_uplay = {}
  match = 0
    
  with open('data/sheet_raw.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
      discord = row['Discord Username (in 0utli3r\'s discord)']
      uplay = row['Uplay Username']
      discord_to_uplay[discord] = uplay
  
  for team in best_combos:
    match += 1
    team1 = []
    team2 = []

    for user in team[0][1:]:
      user = user[0]
      try:
        uplay = discord_to_uplay[user]
        player = f'Discord: {user} - Uplay: {uplay}'
      except:
        player = user
      team1.append(player)
    
    for user in team[1][1:]:
      user = user[0]
      try:
        uplay = discord_to_uplay[user]
        player = f'Discord: {user} - Uplay: {uplay}'
      except:
        player = user
      team2.append(player)

    print(f'Match {match}:')
    for player in team1:
      print(player)
    print('vs')
    for player in team2:
      print(player)
    print()

def main_func():
  while get_matchups(players) >= 10:
    print('\n\n\n')

main_func()

#cProfile.runctx('main_func()', globals(),locals())

def test(runtime_num):
  for i in range(runtime_num):
    main_func()
