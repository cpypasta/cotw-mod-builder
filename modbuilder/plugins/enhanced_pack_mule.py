from typing import List

DEBUG = False
NAME = "Enhanced Pack Mule"
DESCRIPTION = "Increases the weight you can carry. You must have the Pack Mule skill unlocked for this modification to take affect."
FILE = "settings/hp_settings/player_skills.bin"
OPTIONS = [
  { "name": "Weight", "min": 24.0, "max": 99.9, "default": 23.0, "initial": 99.9 }
]
  
def format(options: dict) -> str:
  return f"Enhanced Pack Mule ({options['weight']}kg)"

def update_values_at_offset(options: dict) -> List[dict]:
  updated_value = options['weight']
  return [{
    "offset": 22176,
    "value": f"set_player_carry_capacity({updated_value})"
  }]