from typing import List

DEBUG = True
NAME = "Enhanced Soft Feet"
DESCRIPTION = "Decreases the noise you generate when moving through foiliage (grass and leaves) and vegetation (bushes and shrubs). You must have the Soft Feet skill unlocked for this modification to take affect."
FILE = "settings/hp_settings/player_skills.bin"
OPTIONS = [
  { "name": "Soft Feet Percent", "min": 20, "max": 100, "default": 20, "initial": 100, "increment": 1 }
]

def format(options: dict) -> str:
  sound = options['soft_feet_percent']
  return f"Enhanced Soft Feet ({int(sound)}%)"

def update_values_at_offset(options: dict) -> List[dict]:
  updated_value = round(1.0 - options['soft_feet_percent'] / 100,1)
  return [
    {
      "offset": 17864,
      "value": f"set_material_noise_multiplier({updated_value})"
    },
    {
      "offset": 17904,
      "value": f"set_material_noise_multiplier({updated_value}), set_vegetation_noise_multiplier({updated_value})"
    }
  ]