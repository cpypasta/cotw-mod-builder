from typing import List
from modbuilder import mods
from pathlib import Path
from deca.ff_rtpc import rtpc_from_binary, RtpcNode, RtpcProperty

DEBUG = False
NAME = "Increase Diamond Spawns"
DESCRIPTION = "This will increase the chances of having a killed animal respawn as a diamond. I would recommend you start with a fresh population (delete old population file)."
FILE = "global/global_animal_types.blo"
OPTIONS = [
  { "name": "Diamond Chances", "style": "list", "default": "medium", "initial": ["low", "medium", "high"] }
]

def format(options: dict) -> str:
  return f"Increase Diamond Spawns ({options['diamond_chances']})"

def open_rtpc(filename: Path) -> RtpcNode:
  with filename.open("rb") as f:
    data = rtpc_from_binary(f) 
  root = data.root_node
  return root.child_table[0].child_table

def process(options: dict) -> None:
  respawn_level = options['diamond_chances']
  if respawn_level == 'low':
    respawn_level = 0.02
  elif respawn_level == "medium":
    respawn_level = 0.05
  else:
    respawn_level = 0.1
    
  animals = open_rtpc(mods.APP_DIR_PATH / "mod/dropzone" / FILE)
  for animal in animals:
    i = 0
    table_index = None
    max_i = len(animal.child_table)
    while not table_index and i < max_i:
      table_type = animal.child_table[i].prop_table[0].data
      if type(table_type) == bytes and table_type.decode("utf-8") == 'CAnimalTypeScoringSettings':
        table_index = i
        break
      else:
        i = i + 1        
    
    if table_index == None:
      continue        
    
    score_details = animal.child_table[table_index].child_table
    for score_node in score_details:
      score_type = score_node.prop_table[1].data    
      if type(score_type) == bytes and score_type.decode("utf-8") == "SAnimalTypeScoringDistributionSettings":
        score_high = score_node.prop_table[-3].data        
        if score_high > 0:
          score_max_weight = score_node.prop_table[2].data
          score_weight_bias_pos = score_node.prop_table[-2].data_pos
          weight_bias = round(score_max_weight * respawn_level, 2)
          mods.update_file_at_offset(Path(FILE), score_weight_bias_pos, weight_bias)
  