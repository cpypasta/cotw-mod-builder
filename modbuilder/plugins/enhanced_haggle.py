from typing import List

DEBUG=False
NAME = "Enhanced Haggle"
DESCRIPTION = "Reduce the cost of all items for sale in the store. The haggle percentage is the amount the prices are lowered. At 100 percent, all items in the store are free. You must have the Haggle skill unlocked for this modification to take affect."
FILE = "settings/hp_settings/player_skills.bin"
OPTIONS = [
  { "name": "Haggle Percent", "min": 5, "max": 100, "default": 5, "increment": 5 }  
]

def format(options: dict) -> str:
  haggle = options["haggle_percent"]
  return f"Enhanced Haggle ({int(haggle)}%)"

def update_values_at_offset(options: dict) -> List[dict]:
  updated_value = int(options['haggle_percent'])
  return [
    {
      "offset": 21064,
      "value": f"haggle({updated_value})"
    }
  ]