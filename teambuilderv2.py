from itertools import combinations, product
from collections import namedtuple
from tqdm import tqdm
import random
import json
import csv
import sys
import cProfile
import os
import math
from numba import jit,njit


players = { 'Aliossz':2400, 'BERSERK.ENTELOS':2300, 'dontcussim5':2300, 'lil_broomstick':2300, 'passwordis12345':2800, 'fusedProdigy':3600, 'T-huntbot':2800, 'runmedome':2300, 'notTheos':2100, 'mexdex':2300, 'j3lly':3600, 'nigelfarage':3600, 'eduva':2800, 'the_camel4':2300, 'amdthreadripper':1800, 'ohmoose':2800, 'kophosis':2800, 'kj_roman':2600, 'spectrum':2400, 'twizillerhat':2400, 'cryptospartan':2300, 'coach':3200, 'dinkster':3400, 'player01':1800, 'player02':2000, 'player03':3000, 'player04':2500, 'player05':1900, 'player06':1800, 'player07':2100, 'player08':4000, 'player09':2600, 'player10':3500, 'player11':3200, 'player12':2500, 'player13':2700, 'player14':2600, 'player15':2300, 'player16':2500, 'player17':1900}#, 'player18':2500, 'player19':3100, 'player20':2900}#, 'player21':2200, 'player22':2000, 'player23':2400, 'player24':3200, 'player25':2600, 'player26':2800}#, 'player27':3000, 'player28':3600 }
players = list(players.items())
random.shuffle(players)
players = dict(players)

#full_result_list = [dict(x) for x in combinations(players.items(), 5)]

possible_team = namedtuple('possible_team', ('players','team_rating'))

#result_gen = (possible_team(set(y),z) for x in combinations(players.items(), 5) for y,z in zip(*x))

#result_gen = (possible_team(set(next(y)),next(y)) for x in combinations(players.items(), 5) if (y := zip(*x)) )

#result_gen = (possible_team(set(next(z)),next(z)) for z in iter(y for x in combinations(players.items(), 5) for y in zip(*x)))

def result_gen(reverse=False):
    if reversed:
        players_dict = reversed(players.items())
    else:
        players_dict = players.items()

    for x in combinations(players_dict, 5):
        y,z = zip(*x)
        y,z = set(y),sum(z)
        yield possible_team(y,z)

forward_gen = result_gen()

reverse_gen = result_gen(reverse=True)

"""for x,y in product(forward_gen, reverse_gen):
    print(x,y)
    break"""

#print(next(result_gen))
#print(next(result_gen))
#first_team = next(result_gen)
#print(first_team)
#print(sum(first_team[1]))
def create_matchup():
    for t1_players, t1_rating in forward_gen:
        find = False
        reverse_gen = result_gen(reverse=True)

        for t2_players, t2_rating in reverse_gen:
            shared_players = t1_players & t2_players
          
            if not shared_players:
                difference = abs(t1_rating - t2_rating)

                if difference == 0:
                    print(t1_players,t2_players)
                    print(t1_rating,t2_rating)
                    return # something

create_matchup()
#print(next(forward_gen))
#print(next(reverse_gen))