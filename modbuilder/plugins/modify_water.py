from typing import List

DEBUG=False
NAME = "Modify Water"
DESCRIPTION = "This mod allows you to walk under the water. Jumping under water will make you jump super high. Either do not jump, or use the Impact Resistance mod to keep yourself alive. Player speed mods will interact with the player movement under water."
FILE = "settings/hp_settings/player_deep_water_handling.bin"
OPTIONS = [
    { 
     "name": "Max Depth", 
     "style": "slider", 
     "min": 1.0, 
     "max": 50.0, 
     "initial": 1.0,
     "increment": 1.0,
     "note": "how deep you can go before you cannot move",
     "recommend": 28
    },    
    { 
     "name": "Player Movement", 
     "style": "slider", 
     "min": -1500.0, 
     "max": 0.0, 
     "initial": -90,
     "increment": 1.0,
     "note": "how much player slows down in water",
     "recommend": -4
    },
    { 
     "name": "Jump Height", 
     "style": "slider", 
     "min": -100.0, 
     "max": 1.0, 
     "initial": 1.0,
     "increment": 1.0,
     "note": "doesn't seem to do anything, but you are welcome to try",
    },    
]
PRESETS = [
  { 
   "name": "Game Defaults", 
   "options": [
     {"name": "max_depth", "value": 1.0}, 
     {"name": "player_movement", "value": -90.0}, 
     {"name": "jump_height", "value": 1.0}
    ] 
  },
  { 
   "name": "Recommended without speed mod", 
   "options": [
     {"name": "max_depth", "value": 28.0}, 
     {"name": "player_movement", "value": -4.0}, 
     {"name": "jump_height", "value": 1.0}
    ] 
  },
  { 
   "name": "Recommended with 2x speed mod", 
   "options": [
     {"name": "max_depth", "value": 28.0}, 
     {"name": "player_movement", "value": -500.0}, 
     {"name": "jump_height", "value": 1.0}
    ] 
  },  
]

def format(options: dict) -> str:
  max_depth = int(options["max_depth"])
  player_movement = int(options["player_movement"])
  jump_height = int(options["jump_height"])
  return f"Water ({max_depth} depth, {player_movement} speed, {jump_height} jump)"

def update_values_at_offset(options: dict) -> List[dict]:
  return [
    {
      "offset": 640, # maxDepth
      "value": 100.0
    },
    {
      "offset": 648, # targetedMovement
      "value": -4.0
    },
    {
      "offset": 652, # targetedJumpHeight
      "value": 1.0
    }
  ]