from typing import List

DEBUG = False
NAME = "Decrease Hunting Pressure"
DESCRIPTION = "Decreases hunting pressure that is created from killing animals."
FILE = "settings/hp_settings/global_simulation.bin"
OPTIONS = [
  { "name": "Decrease Pressure Radius", "type": int, "min": 0, "max": 128, "default": 128, "increment": 1, "initial": 128 },
  { "name": "Decrease Pressure Amount Percent", "type": int, "min": 0, "max": 100, "default": 0, "increment": 5, "initial": 10 }
]

def format(options: dict) -> str:
  decrease_pressure_radius = int(options['decrease_pressure_radius'])
  decrease_pressure_amount_percent = int(options['decrease_pressure_amount_percent'])
  return f"Decrease Hunting Pressure ({decrease_pressure_radius}m, {decrease_pressure_amount_percent}%)"

def update_values_at_offset(options: dict) -> List[dict]:
  decrease_pressure_radius = options['decrease_pressure_radius']
  decrease_pressure_amount_percent = 1.0 - options['decrease_pressure_amount_percent'] / 100
  return [
    {
      "offset": 788,
      "value": decrease_pressure_radius
    },
    {
      "offset": 792,
      "transform": "multiply",
      "value": decrease_pressure_amount_percent
    }
  ]