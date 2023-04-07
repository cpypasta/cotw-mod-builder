from typing import List

DEBUG = False
NAME = "Increase Cash Reward"
DESCRIPTION = "Increase the cash reward when harvesting kills."
FILE = "settings/hp_settings/player_rewards.bin"
OPTIONS = [
  { "name": "Cash Reward Multiplier", "type": int, "min": 2, "max": 50, "default": 1, "increment": 1 }
]

def format(options: dict) -> str:
  cash_reward_multiplier = int(options['cash_reward_multiplier'])
  return f"Increase Cash Reward ({cash_reward_multiplier}x)"

def update_values_at_offset(options: dict) -> List[dict]:
  cash_reward_multiplier = int(options['cash_reward_multiplier'])
  if cash_reward_multiplier < 10:
    cash_reward_multiplier = f" {cash_reward_multiplier}"
  return [
    {
      "offset": 57168,
      "value": f"Cash reward = (( Normalized Weight * Cash Span ) + Base Cash ) * Species Cash MP * (({cash_reward_multiplier} - Skill Value Cash MP) + (Skill Value Cash MP * Skill Value))"
    }
  ]