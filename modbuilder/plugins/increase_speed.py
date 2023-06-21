from typing import List

# verified
NAME = "Increase Speed"
DESCRIPTION = "Increase the speed of the player when standing, crouching, and when prone."
FILE = "editor/entities/hp_characters/main_characters/elmer/elmer_movement.mtunec"
OPTIONS = [
  { "name": "Stand Speed Multiplier", "min": 1.0, "max": 10.0, "default": 1, "increment": 0.1 },
  { "name": "Crouch Speed Multiplier", "min": 1.0, "max": 10.0, "default": 1, "increment": 0.1 },
  { "name": "Prone Speed Multiplier", "min": 1.0, "max": 10.0, "default": 1, "increment": 0.1 }
]

def format(options: dict) -> str:
  stand_multiplier = options['stand_speed_multiplier']
  crouch_multiplier = options['crouch_speed_multiplier']
  prone_multiplier = options['prone_speed_multiplier']
  return f"Increase Speed ({round(stand_multiplier, 1)}x, {round(crouch_multiplier, 1)}x, {round(prone_multiplier, 1)}x)"

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