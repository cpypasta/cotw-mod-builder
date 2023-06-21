from typing import List
from modbuilder import mods

DEBUG = True
NAME = "Modify Animal Senses"
DESCRIPTION = "Modify how animals sense and respond to you. The thresholds determine when the animal enters and exits various behavioral states. The higher the threshold, the longer it takes to enter into that state."
FILE = "settings/hp_settings/animal_senses.bin"
OPTIONS = [
  { "name": "Increase Attentiveness Threshold Percent", "min": 0, "max": 300, "default": 0, "increment": 10 },
  { "name": "Increase Alert Threshold Percent", "min": 0, "max": 300, "default": 0, "increment": 10 },
  { "name": "Increase Alarmed Threshold Percent", "min": 0, "max": 300, "default": 0, "increment": 10 },
  { "name": "Increase Defensive Threshold Percent", "min": 0, "max": 300, "default": 0, "increment": 10 },
  { "name": "Reduce Nervous Duration Percent", "min": 0, "max": 100, "default": 0, "increment": 1 },
  { "name": "Reduce Defensive Duration Percent", "min": 0, "max": 100, "default": 0, "increment": 1 }
]

def format(options: dict) -> str:
  attentive_percent = int(options['increase_attentiveness_threshold_percent'])
  alert_percent = int(options['increase_alert_threshold_percent'])
  alarmed_percent = int(options['increase_alarmed_threshold_percent'])
  defensive_percent = int(options['increase_defensive_threshold_percent'])
  return f"Modify Animal Senses ({attentive_percent}%, {alert_percent}%, {alarmed_percent}%, {defensive_percent}%)"

def update_values_at_offset(options: dict) -> List[dict]:
  attentive_percent = 1 + options['increase_attentiveness_threshold_percent'] / 100
  alert_percent = 1 + options['increase_alert_threshold_percent'] / 100
  alarmed_percent = 1 + options['increase_alarmed_threshold_percent'] / 100
  defensive_percent = 1 + options['increase_defensive_threshold_percent'] / 100
  nervous_duration_percent = 1 - options['reduce_nervous_duration_percent'] / 100
  default_defensive_duration_percent = options['reduce_defensive_duration_percent'] if "reduce_defensive_duration_percent" in options else 0
  defensive_duration_percent = 1 - default_defensive_duration_percent / 100
  
  nervous_min = 600.0
  nervous_max = 900.0
  defensive_min_easy = 18.0
  defensive_min = 23.0
  defensive_max_easy = 22.0
  defensive_max = 27.0
  new_nervous_min = float(round(nervous_min * nervous_duration_percent))
  new_nervous_max = float(round(nervous_max * nervous_duration_percent))
  new_defensive_min_easy = float(round(defensive_min_easy * defensive_duration_percent))
  new_defensive_min = float(round(defensive_min * defensive_duration_percent))
  new_defensive_max_easy = float(round(defensive_max_easy * defensive_duration_percent))
  new_defensive_max = float(round(defensive_max * defensive_duration_percent))
  new_defensive_min_easy_cell = mods.find_closest_lookup(new_defensive_min_easy, FILE)
  new_defensive_min_cell = mods.find_closest_lookup(new_defensive_min, FILE)
  new_defensive_max_easy_cell = mods.find_closest_lookup(new_defensive_max_easy, FILE)
  new_defensive_max_cell = mods.find_closest_lookup(new_defensive_max, FILE)
  new_nervous_min_offset = 140240
  new_nervous_max_offset = 140244
  new_defensive_min_easy_offset = 13988
  new_defensive_min_offset = 14340
  new_defensive_max_easy_offset = 14692
  new_defensive_max_offset = 15044
  
  attentive_enter = 0.20000000298023224
  attentive_exit = 0.10000000149011612    
  alert_enter = 0.5                    
  alert_exit = 0.400000005960464
  alarmed_enter = 1.29999995231628
  alarmed_exit = 1.20000004768372
  defensive_enter = 1.70000004768372
  defensive_exit = 1.600000023841858
  new_attentive_enter_cell = mods.find_closest_lookup(attentive_enter * attentive_percent, FILE)
  new_attentive_exit_cell = mods.find_closest_lookup(attentive_exit * attentive_percent, FILE)
  new_alert_enter_cell = mods.find_closest_lookup(alert_enter * alert_percent , FILE)
  new_alert_exit_cell = mods.find_closest_lookup(alert_exit * alert_percent, FILE)
  new_alarmed_enter_cell = mods.find_closest_lookup(alarmed_enter * alarmed_percent, FILE)
  new_alarmed_exit_cell = mods.find_closest_lookup(alarmed_exit * alarmed_percent, FILE)
  new_defensive_enter_cell = mods.find_closest_lookup(defensive_enter * defensive_percent, FILE)
  new_defensive_exit_cell = mods.find_closest_lookup(defensive_exit * defensive_percent , FILE)
  attentive_enter_offset = 10468
  attentive_exit_offset = 10820
  alert_enter_offset = 11172
  alert_exit_offset = 11524
  alarmed_enter_offset = 11876
  alarmed_exit_offset = 12228
  defensive_enter_offset = 12580
  defensive_exit_offset = 12932
  
  return [
    {
      "offset": new_nervous_min_offset,
      "value": new_nervous_min
    },
    {
      "offset": new_nervous_max_offset,
      "value": new_nervous_max
    },
    {
      "offset": new_defensive_min_easy_offset,
      "value": new_defensive_min_easy_cell
    },
    {
      "offset": new_defensive_min_offset,
      "value": new_defensive_min_cell
    },
    {
      "offset": new_defensive_max_easy_offset,
      "value": new_defensive_max_easy_cell
    },
    {
      "offset": new_defensive_max_offset,
      "value": new_defensive_max_cell
    },
    {
      "offset": attentive_enter_offset,
      "value": new_attentive_enter_cell
    },
    {
      "offset": attentive_exit_offset,
      "value": new_attentive_exit_cell
    },
    {
      "offset": alert_enter_offset,
      "value": new_alert_enter_cell
    },
    {
      "offset": alert_exit_offset,
      "value": new_alert_exit_cell
    },
    {
      "offset": alarmed_enter_offset,
      "value": new_alarmed_enter_cell
    },
    {
      "offset": alarmed_exit_offset,
      "value": new_alarmed_exit_cell
    },
    {
      "offset": defensive_enter_offset,
      "value": new_defensive_enter_cell
    },
    {
      "offset": defensive_exit_offset,
      "value": new_defensive_exit_cell
    }
  ]