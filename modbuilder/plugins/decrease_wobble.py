from typing import List

NAME = "Decrease Wobble"
DESCRIPTION = "Reduce the amount of wobble when looking through the scope."
FILE = "editor/entities/hp_characters/main_characters/elmer/elmer_movement.mtunec"
OPTIONS = [
  { "name": "Reduce Stand Percent", "type": int, "min": 0, "max": 100, "default": 0, "increment": 5 },
  { "name": "Reduce Crouch Percent", "type": int, "min": 25, "max": 100, "default": 25, "increment": 5 },
  { "name": "Reduce Prone Percent", "type": int, "min": 50, "max": 100, "default": 50, "increment": 5 }
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