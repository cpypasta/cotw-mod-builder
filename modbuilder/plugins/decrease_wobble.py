from typing import List

DEBUG = False
NAME = "Decrease Wobble"
DESCRIPTION = "Reduce the amount of wobble when looking through the scope."
FILE = "editor/entities/hp_characters/main_characters/elmer/elmer_movement.mtunec"
OPTIONS = [
  { "name": "Reduce Stand Percent", "min": 0, "max": 100, "default": 0, "increment": 5 },
  { "name": "Reduce Crouch Percent", "min": 25, "max": 100, "default": 25, "increment": 5 },
  { "name": "Reduce Prone Percent", "min": 50, "max": 100, "default": 50, "increment": 5 }
]
PRESETS = [
  { "name": "Game Defaults", "options": [
    { "name": "reduce_stand_percent", "value": 0 },
    { "name": "reduce_crouch_percent", "value": 25 },
    { "name": "reduce_prone_percent", "value": 50 }
  ]},
  { "name": "Recommended", "options": [
    { "name": "reduce_stand_percent", "value": 25 },
    { "name": "reduce_crouch_percent", "value": 70 },
    { "name": "reduce_prone_percent", "value": 100 }
  ]}
]

def format(options: dict) -> str:
  stand_percent = options['reduce_stand_percent']
  crouch_percent = options['reduce_crouch_percent']
  prone_percent = options['reduce_prone_percent']
  return f"Decrease Wobble ({int(stand_percent)}%, {int(crouch_percent)}%, {int(prone_percent)}%)"

def update_values_at_offset(options: dict) -> List[dict]:
  stand_percent = options['reduce_stand_percent']
  crouch_percent = options['reduce_crouch_percent']
  prone_percent = options['reduce_prone_percent']
  stand_value = round(1.0 - stand_percent / 100, 1)
  crouch_value = round(1.0 - crouch_percent / 100, 1)
  prone_value = round(1.0 - prone_percent / 100, 1)
  return [
    {
      "offset": 444,
      "value": stand_value
    },
    {
      "offset": 448,
      "value": crouch_value
    },
    {
      "offset": 452,
      "value": prone_value
    }
  ]