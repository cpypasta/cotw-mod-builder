from typing import List

NAME = "Enhanced Impact Resistance"
DESCRIPTION = "Decreases damage from falling. You must have the Impact Resistance skill unlocked for this modification to take affect."
FILE = "settings/hp_settings/player_skills.bin"
OPTIONS = [
  { "name": "Fall Damage Reduction Percent", "type": int, "min": 30, "max": 90, "default": 20, "increment": 10 }
]

def format(options: dict) -> str:
  damage_reduce = options['fall_damage_reduction_percent']
  updated_value = 1.0 - damage_reduce / 100
  return f"Enhanced Impact Resistance ({int(damage_reduce)}%, {round(updated_value,1)})"

def update_values_at_offset(options: dict) -> List[dict]:
  updated_value = round(1.0 - options['fall_damage_reduction_percent'] / 100, 1)
  return [
    {
      "offset": 19872,
      "value": f"reduce_player_fall_damage({updated_value})"
    }
  ]