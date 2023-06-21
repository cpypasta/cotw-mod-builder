from typing import List

DEBUG=True
NAME = "Enhanced Improvised Blind"
DESCRIPTION = "Further decreases your visibility when hiding in large bushes and shrubs. You must have the Improvised Blind skill unlocked for this modification to take affect."
FILE = "settings/hp_settings/player_skills.bin"
OPTIONS = [
  { "name": "Vegetation Camoflauge Percent", "max": 890, "min": 60, "default": 50, "increment": 10 }
]
  
def format(options: dict) -> str:
  camo = options["vegetation_camoflauge_percent"]
  return f"Enhanced Improvised Blind ({int(camo)}%)"

def update_values_at_offset(options: dict) -> List[dict]:
  updated_value = 1.0 + options['vegetation_camoflauge_percent'] / 100
  return [{
    "offset": 18240,
    "value": f"increase_vegetation_camo({updated_value})"
  }]