from typing import List

NAME = "Increase Speed"
DESCRIPTION = "Increase the speed of the player when standing, crouching, and when prone."
FILE = "editor/entities/hp_characters/main_characters/elmer/elmer_movement.mtunec"
OPTIONS = [
  { "name": "Stand Speed Multiplier", "type": int, "min": 1, "max": 10, "default": 1, "increment": 0.5 },
  { "name": "Crouch Speed Multiplier", "type": int, "min": 1, "max": 10, "default": 1, "increment": 0.5 },
  { "name": "Prone Speed Multiplier", "type": int, "min": 1, "max": 10, "default": 1, "increment": 0.5 }
]

def format(options: dict) -> str:
  stand_multiplier = options['stand_speed_multiplier']
  crouch_multiplier = options['crouch_speed_multiplier']
  prone_multiplier = options['prone_speed_multiplier']
  return f"Increase Speed ({int(stand_multiplier)}x, {int(crouch_multiplier)}x, {int(prone_multiplier)}x)"

def update_values_at_offset(options: dict) -> List[dict]:
  stand_multiplier = options['stand_speed_multiplier']
  crouch_multiplier = options['crouch_speed_multiplier']
  prone_multiplier = options['prone_speed_multiplier']
  return [
    {
      "offset": 176,
      "transform": "multiply",
      "value": stand_multiplier
    },
    {
      "offset": 200,
      "transform": "multiply",
      "value": stand_multiplier
    },
    {
      "offset": 184,
      "transform": "multiply",
      "value": crouch_multiplier
    },
    {
      "offset": 208,
      "transform": "multiply",
      "value": crouch_multiplier
    },
    {
      "offset": 192,
      "transform": "multiply",
      "value": prone_multiplier
    },
    {
      "offset": 216,
      "transform": "multiply",
      "value": prone_multiplier
    }
  ]