from typing import List

DEBUG = False
NAME = "Increase Cash Reward"
DESCRIPTION = "Increase the cash reward when harvesting kills."
FILE = "settings/hp_settings/player_rewards.bin"
OPTIONS = [
  { "name": "Cash Reward Multiplier", "min": 2, "max": 20, "default": 1, "increment": 1 }
]

def format(options: dict) -> str:
  cash_reward_multiplier = int(options['cash_reward_multiplier'])
  return f"Increase Cash Reward ({cash_reward_multiplier}x)"

def update_values_at_offset(options: dict) -> List[dict]:
  cash_reward_multiplier = options['cash_reward_multiplier']
  return [
    {
      "offset": 62244,
      "transform": "multiply",
      "value": cash_reward_multiplier
    },
    {
      "offset": 62408,
      "transform": "multiply",
      "value": cash_reward_multiplier
    }
  ]