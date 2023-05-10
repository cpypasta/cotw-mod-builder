from typing import List

DEBUG=True
NAME = "Decrease Resting Cost"
DESCRIPTION = "Decrease the resting cost as well as how quickly the cost rises. The multiplier values control how the cost of resting increases if done too frequently. You can change the frequency by decreasing the time to decrease cost."
FILE = "settings/hp_settings/resting_data.bin"
OPTIONS = [
  { "name": "Decrease Cost", "min": 0, "max": 250, "default": 250, "increment": 1, "initial": 250 },
  { "name": "Decrease Cost Multiplier", "min": 0, "max": 2, "default": 2, "increment": 1, "initial": 2 },
  { "name": "Decrease Max Cost Multiplier", "min": 0, "max": 10, "default": 10, "increment": 1, "initial": 10 },
  { "name": "Decrease Time to Reduce Cost", "min": 0, "max": 7200, "default": 7200, "increment": 2, "initial": 7200, "note": "seconds" }  
]

def format(options: dict) -> str:
  cost = int(options["decrease_cost"])
  cost_multiplier = int(options["decrease_cost_multiplier"])
  cost_max_multiplier = int(options["decrease_max_cost_multiplier"])
  cost_time = int(options["decrease_time_to_reduce_cost"])
  return f"Decrease Resting Cost ({cost}, {cost_multiplier}x, {cost_max_multiplier}x, {cost_time}s)"

def update_values_at_offset(options: dict) -> List[dict]:
  cost = options["decrease_cost"]
  cost_multiplier = options["decrease_cost_multiplier"]
  cost_max_multiplier = options["decrease_max_cost_multiplier"]
  cost_time = options["decrease_time_to_reduce_cost"]
  
  return [
    {
      "offset": 572,
      "value": cost_multiplier
    },    
    {
      "offset": 576,
      "value": cost_max_multiplier
    },    
    {
      "offset": 568,
      "value": cost
    },    
    {
      "offset": 580, 
      "value": cost_time
    }
  ]