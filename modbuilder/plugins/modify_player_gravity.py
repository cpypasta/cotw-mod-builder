from typing import List

DEBUG=False
NAME = "Modify Player Gravity"
DESCRIPTION = "Allows you to adjust the effect of gravity on your player. You will definitely want to use the Impact Resistance mod with this one."
FILE = "settings/player.bin"
OPTIONS = [
    {
        "name": "Gravity",
        "min": -50.0,
        "max": 50.0,
        "default": -21.0,
        "increment": 1.0,
        "initial": -21.0,
        "note": "lower the number the more gravity"
    }
]
PRESETS = [
    {
        "name": "Game Defaults",
        "options": [
            {"name": "gravity", "value": -21.0}
        ]
    },
    {
        "name": "Just a Little",
        "options": [
            {"name": "gravity", "value": 0.0}
        ]
    },
    {
        "name": "Jump on Cabins",
        "options": [
            {"name": "gravity", "value": -8.0}
        ]
    },    
    {
        "name": "Above the Trees",
        "options": [
            {"name": "gravity", "value": -4.0}
        ]
    },    
    {
        "name": "Super Human",
        "options": [
            {"name": "gravity", "value": -1.0}
        ]
    },
    {
        "name": "Astronaut",
        "options": [
            {"name": "gravity", "value": 1.0}
        ]
    }    
]

def format(options: dict) -> str:
  return f"Modify Player Gravity ({options['gravity']})"

def update_values_at_offset(options: dict) -> List[dict]:
    return [
        {
            "offset": 1949, # gravity
            "value": options["gravity"]
        }                       
    ]