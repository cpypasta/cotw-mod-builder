from typing import List

NAME = "Enhanced Fatal Attraction"
DESCRIPTION = "Increases chance of attracting animals and causing a vocalization response when using callers. You must have both of the Fatal Attraction skill tiers unlocked for this modification to take affect."
FILE = "settings/hp_settings/player_skills.bin"
OPTIONS = [
  { "name": "Increase Caller Attraction Percent", "min": 200, "max": 2000, "default": 200, "increment": 10 }  
]

def format(options: dict) -> str:
  attraction = options["increase_caller_attraction_percent"]
  return f"Enhanced Fatal Attraction ({int(attraction)}%)"

def update_values_at_offset(options: dict) -> List[dict]:
  attraction_percent = options["increase_caller_attraction_percent"] / 100
  return [
    {
      "offset": 20072,
      "value": f"caller_attraction_probability({attraction_percent:0>4.1f}),caller_response_probability(ALL,{attraction_percent:0>4.1f})"
    }
  ]