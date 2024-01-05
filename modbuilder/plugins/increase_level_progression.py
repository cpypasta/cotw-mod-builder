from typing import List
from modbuilder import mods

DEBUG=False
NAME = "Increase Level Progression"
DESCRIPTION = "Increases skill and perk points you gain when increasing your character's level. This mod will increase the progession such that you are able to unlock every skill and perk. This mod will not change your existing character's skill and perk points."
FILE = "settings/hp_settings/player_rewards.bin"
OPTIONS = [
  { "title": "There are no options. Just add the modification." }
]

def format(options: dict) -> str:
  return "Increase Level Progression"

# there are a total of 24 perks and 26 skills; game only gives you 23 of each
# max is 45 for each to get everything

def process(options: dict) -> None:
  indices = [556,572,596,612,636,652,676,692,716,732,756,772,796,812,836,852,876,892,916,932,956,972,996,1012,1036,1052,1076,1092,1116,1132,1156,1172,1196,1212,1236,1252,1276,1292,1332,1356,1396,1412,1452,1476]
  mods.update_file_at_offsets(FILE, indices, 11)