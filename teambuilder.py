from itertools import combinations
from tqdm import tqdm
import random
import json
import csv
import sys
import cProfile
import os
import math
from numba import jit,njit


print('START')
print('------------------------------'*10)
print()


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
  #full_result_list = list(map(dict, combinations(players.items(), 5)))
  if groups:
    result_list = groups_on_same_team(players,groups,full_result_list)
  else:
    result_list = full_result_list
  
  result_list_len = len(result_list)
  full_result_list = []

  print(f'Possible Teams: {result_list_len:,}')
  print(f'{math.comb(len(players), 5):,}')
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

      playerlist_check = set(teamcheck.keys())
      shared_players = playerlist_check & playerlist
      
      if not shared_players:
        team2_total = sum(teamcheck.values())
        difference = abs(team1_total - team2_total)
        
        if difference <= difference_best:
          
          game = []
          difference_best = difference
          combo['total'] = team1_total
          teamcheck['total'] = team2_total
          combo_sorted = sorted(combo.items(), key=lambda_sort(), reverse=True)
          teamcheck_sorted = sorted(teamcheck.items(), key=lambda_sort(), reverse=True)

          #if ((combo_sorted[1][1] > teamcheck_sorted[1][1] and combo_sorted[2][1] > teamcheck_sorted[2][1]) \
           # or (teamcheck_sorted[1][1] > combo_sorted[1][1] and teamcheck_sorted[2][1] > combo_sorted[2][1])):
          if ((abs((combo_sorted[1][1] + combo_sorted[2][1] + combo_sorted[3][1]) - (teamcheck_sorted[1][1] + teamcheck_sorted[2][1] + teamcheck_sorted[3][1]))) > 200) \
          or ((combo_sorted[1][1] > teamcheck_sorted[1][1] and combo_sorted[2][1] > teamcheck_sorted[2][1]) or (teamcheck_sorted[1][1] > combo_sorted[1][1] and teamcheck_sorted[2][1] > combo_sorted[2][1])):
            del combo['total']
            del teamcheck['total']
            continue

          game.append(combo_sorted)
          game.append(teamcheck_sorted)
          game.append(f'difference: {difference}')
          #game.append('difference: %s' % (difference))
                    
          for key in combo:
            if key != 'total':
              del players[key]
          for key in teamcheck:
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
  players = { 'Aliossz':2400, 'BERSERK.ENTELOS':2300, 'dontcussim5':2300, 'lil_broomstick':2300, 'passwordis12345':2800, 'fusedProdigy':3600, 'T-huntbot':2800, 'runmedome':2300, 'notTheos':2100, 'mexdex':2300, 'j3lly':3600, 'nigelfarage':3600, 'eduva':2800, 'the_camel4':2300, 'amdthreadripper':1800, 'ohmoose':2800, 'kophosis':2800, 'kj_roman':2600, 'spectrum':2400, 'twizillerhat':2400, 'cryptospartan':2300, 'coach':3200, 'dinkster':3400, 'player01':1800, 'player02':2000, 'player03':3000, 'player04':2500, 'player05':1900, 'player06':1800, 'player07':2100, 'player08':4000, 'player09':2600, 'player10':3500, 'player11':3200, 'player12':2500, 'player13':2700, 'player14':2600, 'player15':2300, 'player16':2500, 'player17':1900}#, 'player18':2500, 'player19':3100, 'player20':2900}#, 'player21':2200, 'player22':2000, 'player23':2400, 'player24':3200, 'player25':2600, 'player26':2800}#, 'player27':3000, 'player28':3600 }
  #players = json.load(open('players.json'))

  while get_matchups(players) >= 10:
    print('\n\n\n')

main_func()

#cProfile.runctx('main_func()', globals(),locals())

def test(runtime_num):
  for i in range(runtime_num):
    main_func()
