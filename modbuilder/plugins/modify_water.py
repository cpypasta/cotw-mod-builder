from typing import List
from modbuilder import mods
from pathlib import Path

DEBUG=False
NAME = "Modify Water"
DESCRIPTION = "This mod allows you to walk under the water. Jumping under water will make you jump super high. Either do not jump, or use the Impact Resistance mod to keep yourself alive. Player speed mods will interact with the player movement under water."
BASE_WATER_FILE = "settings/hp_settings/player_deep_water_handling.bin"
WATER_TUNE_FILE = "settings/water_tuning.watertunec"
OPTIONS = [  
    { 
     "name": "Max Depth", 
     "style": "slider", 
     "min": 1.0, 
     "max": 60.0, 
     "initial": 1.0,
     "increment": 1.0,
     "note": "how deep you can go before you cannot move",
    },           
    { 
     "name": "Player Movement", 
     "style": "slider", 
     "min": -100.0, 
     "max": 0.0, 
     "initial": -90,
     "increment": 0.5,
     "note": "how much player slows down in water",
    },
]
PRESETS = [
  { 
   "name": "Game Defaults", 
   "options": [
     {"name": "max_depth", "value": 1.0}, 
     {"name": "player_movement", "value": -90.0}, 
    ] 
  },
  { 
   "name": "Recommended", 
   "options": [
     {"name": "max_depth", "value": 28.0}, 
     {"name": "player_movement", "value": -5.0}, 
    ] 
  },
]

def format(options: dict) -> str:
  max_depth = int(options["max_depth"])
  player_movement = int(options["player_movement"])
  return f"Water ({max_depth} depth, {player_movement} speed)"

def get_files(options: dict) -> list[str]:
  return [BASE_WATER_FILE, WATER_TUNE_FILE]

def process(options: dict) -> None:
  mods.update_file_at_offsets_with_values(
    BASE_WATER_FILE, 
    [(640, options["max_depth"]), (648, options["player_movement"]), (652, 0.0)]
  )
  
  mods.update_file_at_offsets_with_values(
    WATER_TUNE_FILE, 
    [(88, 0.0), (92, 0.0), (96, 28.0)]
  )  