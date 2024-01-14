from typing import List
from modbuilder import mods
from deca.ff_rtpc import rtpc_from_binary

DEBUG=False
NAME = "Modify Weather"
DESCRIPTION = "This mod allows you to control the weather. Select the weather conditions you want to keep."
FILE = "environment/environment_presets_config.bin"

ALL_OPTIONS = []

def set_weather_conditions() -> None:
    global ALL_OPTIONS
    with(open(f"{mods.APP_DIR_PATH}/org/{FILE}", "rb") as f):
        data = rtpc_from_binary(f) 
        condition_nodes = data.root_node.child_table[0].child_table
        conditions = []
        for node in condition_nodes:
            condition = node.prop_table[1].data.decode("utf-8")
            if condition != "base" and not condition.startswith("reserve"):
                conditions.append(condition)
    ALL_OPTIONS = conditions
set_weather_conditions()

OPTIONS = [
    { 
     "name": "Allowed Weather Conditions", 
     "style": "listbox", 
     "values": ALL_OPTIONS,
     "initial": None,
     "size": 5
    }   
]
PRESETS = [
  { 
   "name": "Game Defaults", 
   "options": [
     {"name": "allowed_weather_conditions", "values": list(range(0, len(ALL_OPTIONS))) }
    ] 
  },
  { 
   "name": "Always Sunny", 
   "options": [
     {"name": "allowed_weather_conditions", "values": [ALL_OPTIONS.index("forced_sunny")] }
    ] 
  }   
]

def format(options: dict) -> str:
  return f"Modify Weather ({len(options['allowed_weather_conditions'])} conditions)"

def process(options: dict) -> None:
    with(open(f"{mods.APP_DIR_PATH}/org/{FILE}", "rb") as f):
        data = rtpc_from_binary(f) 
    condition_nodes = data.root_node.child_table[0].child_table    
    allowed_weather_conditions = options['allowed_weather_conditions']
    not_allowed_weather_conditions = []
    for condition_nodes in condition_nodes:
        prop = condition_nodes.prop_table[1]
        condition = prop.data.decode("utf-8")
        if condition == "base":
            continue
        if condition not in allowed_weather_conditions:
            not_allowed_weather_conditions.append((prop.data_pos, "xxx"))
        
    mods.update_file_at_offsets_with_values(FILE, not_allowed_weather_conditions)