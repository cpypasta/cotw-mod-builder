from typing import List

DEBUG = False
NAME = "Increase Speed"
DESCRIPTION = "Increase the speed of the player when standing, crouching, and when prone."
FILE = "editor/entities/hp_characters/main_characters/elmer/elmer_movement.mtunec"
OPTIONS = [
  { "name": "Stand Speed Multiplier", "min": 1.0, "max": 20.0, "default": 1, "increment": 0.1 },
  { "name": "Stand Sprint Speed Multiplier", "min": 1.0, "max": 10.0, "default": 1, "increment": 0.1 },
  { "name": "Crouch Speed Multiplier", "min": 1.0, "max": 20.0, "default": 1, "increment": 0.1 },
  { "name": "Crouch Sprint Speed Multiplier", "min": 1.0, "max": 10.0, "default": 1, "increment": 0.1 },
  { "name": "Prone Speed Multiplier", "min": 1.0, "max": 20.0, "default": 1, "increment": 0.1 },
  { "name": "Prone Sprint Speed Multiplier", "min": 1.0, "max": 10.0, "default": 1, "increment": 0.1 },
  { "name": "Jump Speed Multiplier", "min": 1.0, "max": 20.0, "default": 1, "increment": 0.1 }
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
  stand_sprint_multiplier = options['stand_sprint_speed_multiplier']
  crouch_sprint_multiplier = options['crouch_sprint_speed_multiplier']
  prone_sprint_multiplier = options['prone_sprint_speed_multiplier']  
  jump_multiplier = options['jump_speed_multiplier']
  
  return [
    {
      "offset": 176,
      "transform": "multiply",
      "value": stand_multiplier
    },
    {
      "offset": 180,
      "transform": "multiply",
      "value": stand_sprint_multiplier
    },    
    {
      "offset": 200,
      "transform": "multiply",
      "value": stand_multiplier
    },
    {
      "offset": 204,
      "transform": "multiply",
      "value": stand_sprint_multiplier
    },
    {
      "offset": 184,
      "transform": "multiply",
      "value": crouch_multiplier
    },
    {
      "offset": 188,
      "transform": "multiply",
      "value": crouch_sprint_multiplier
    },    
    {
      "offset": 208,
      "transform": "multiply",
      "value": crouch_multiplier
    },
    {
      "offset": 212,
      "transform": "multiply",
      "value": crouch_sprint_multiplier
    },
    {
      "offset": 192,
      "transform": "multiply",
      "value": prone_multiplier
    },
    {
      "offset": 196,
      "transform": "multiply",
      "value": prone_sprint_multiplier
    },    
    {
      "offset": 216,
      "transform": "multiply",
      "value": prone_multiplier
    },
    {
      "offset": 220,
      "transform": "multiply",
      "value": prone_sprint_multiplier
    },
    {
      "offset": 228,
      "transform": "multiply",
      "value": jump_multiplier
    }    
  ]