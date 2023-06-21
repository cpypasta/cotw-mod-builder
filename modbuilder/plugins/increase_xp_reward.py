from typing import List
from modbuilder import mods

DEBUG = False
NAME = "Increase XP Reward"
DESCRIPTION = "Increase the XP (experience) reward when harvesting kills. There are a few other rewards like finding an artifact and point-of-interest (POI) that also will be increased."
FILE = "settings/hp_settings/player_rewards.bin"
OPTIONS = [
  { "name": "XP Reward Multiplier", "min": 2, "max": 20, "default": 1, "increment": 1 }
]

def format(options: dict) -> str:
  xp_reward_multiplier = int(options['xp_reward_multiplier'])
  return f"Increase XP Reward ({xp_reward_multiplier}x)"

def update_values_at_offset(options: dict) -> List[dict]:
  xp_reward_multiplier = options['xp_reward_multiplier']
  
  reward_lookup_1 = mods.find_closest_lookup(10 * xp_reward_multiplier, FILE)
  reward_lookup_2 = mods.find_closest_lookup(40 * xp_reward_multiplier, FILE)
  
  return [
    {
      "offset": 62224,
      "transform": "multiply",
      "value": xp_reward_multiplier
    },
    {
      "offset": 62400,
      "transform": "multiply",
      "value": xp_reward_multiplier
    },
    {
      "offset": 27092,
      "value": reward_lookup_1
    },
    {
      "offset": 27260,
      "value": reward_lookup_2
    }
  ]