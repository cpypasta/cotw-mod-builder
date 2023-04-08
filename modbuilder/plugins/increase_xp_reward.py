from typing import List

DEBUG = False
NAME = "Increase XP Reward"
DESCRIPTION = "Increase the XP (experience) reward when harvesting kills. There are a few other rewards like finding an artifact and point-of-interest (POI) that also will be increased."
FILE = "settings/hp_settings/player_rewards.bin"
OPTIONS = [
  { "name": "XP Reward Multiplier", "type": int, "min": 2, "max": 20, "default": 1, "increment": 1 }
]

def format(options: dict) -> str:
  xp_reward_multiplier = int(options['xp_reward_multiplier'])
  return f"Increase XP Reward ({xp_reward_multiplier}x)"

def update_values_at_offset(options: dict) -> List[dict]:
  xp_reward_multiplier = options['xp_reward_multiplier']
  return [
    {
      "offset": 59592,
      "transform": "multiply",
      "value": xp_reward_multiplier
    },
    {
      "offset": 59596,
      "transform": "multiply",
      "value": xp_reward_multiplier
    }
  ]