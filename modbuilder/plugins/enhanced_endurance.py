from typing import List

DEBUG = True
NAME = "Enhanced Endurance"
DESCRIPTION = "Reduce how fast your heart rate increases when moving and recovers when resting. At 100 percent, your heart rate does not increase. You must have the Endurance skill unlocked for this modification to take affect."
FILE = "settings/hp_settings/player_skills.bin"
OPTIONS = [
  { "name": "Reduce Heart Rate Percent", "min": 66, "max": 100, "default": 66, "initial": 100, "increment": 1 }  
]

def format(options: dict) -> str:
  endurance = options["reduce_heart_rate_percent"]
  return f"Enhanced Endurance ({int(endurance)}%)"

def update_values_at_offset(options: dict) -> List[dict]:
  endurance_percent = round(options["reduce_heart_rate_percent"] / 100, 2)
  heart_rate_recover = 1 + endurance_percent
  return [
    {
      "offset": 18368,
      "value": f"heart_rate_movement_increase_multiplier({endurance_percent:0<4.2f}), heart_rate_recovery_multiplier({heart_rate_recover:0<4.2f})"
    }
  ]