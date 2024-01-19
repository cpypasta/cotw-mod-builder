from typing import List

DEBUG=False
NAME = "Modify Resting Cost"
DESCRIPTION = "This mod allows you to the reduce the cost of resting. You will need to sleep once to see the changes take effect."
FILE = "settings/hp_settings/resting_data.bin"
OPTIONS = [
    { 
     "name": "Cost", 
     "style": "slider", 
     "min": 1.0, 
     "max": 300.0, 
     "initial": 250.0,
     "increment": 1.0,
     "note": "base cost of resting without any multipliers"
    },   
    { 
     "name": "Increase and Decrease Multiplier", 
     "style": "slider", 
     "min": 1.0, 
     "max": 5.0, 
     "initial": 2.0,
     "increment": 1.0,
     "note": "increase in cost before cooldown; decrease in cost after cooldown"
    },   
    { 
     "name": "Max Increase Multiplier", 
     "style": "slider", 
     "min": 1.0, 
     "max": 15.0, 
     "initial": 10.0,
     "increment": 1.0,
     "note": "max cost increase multiplier"
    },  
    { 
     "name": "Cooldown", 
     "style": "slider", 
     "min": 1.0, 
     "max": 7200.0, 
     "initial": 7200.0,
     "increment": 1.0,
     "note": "amount of time in seconds before decrease multipler is applied"
    },          
]
PRESETS = [
  { 
   "name": "Game Defaults", 
   "options": [
     {"name": "cost", "value": 250.0}, 
     {"name": "increase_and_decrease_multiplier", "value": 2.0}, 
     {"name": "max_increase_multiplier", "value": 10.0},
     {"name": "cooldown", "value": 7200.0},
    ] 
  },  
  { 
   "name": "Cheap", 
   "options": [
     {"name": "cost", "value": 1.0}, 
     {"name": "increase_and_decrease_multiplier", "value": 1.0}, 
     {"name": "max_increase_multiplier", "value": 1.0},
     {"name": "cooldown", "value": 1.0},
    ] 
  },  
]

def format(options: dict) -> str:
  return f"Modify Resting Cost"

def update_values_at_offset(options: dict) -> List[dict]:
  return [
    {
      "offset": 568, # base cost
      "value": 1.0
    },
    {
      "offset": 572, # increase multiplier
      "value": 1.0
    },
    {
      "offset": 572, # increase multiplier
      "value": 1.0
    },    
    {
      "offset": 576, # max_cost_multiplier
      "value": 1.0
    },
    {
      "offset": 580, # time for reduction (seconds)
      "value": 1.0
    }
  ]