from typing import List
from modbuilder import mods
from deca.ff_rtpc import rtpc_from_binary, RtpcNode, RtpcProperty
from pathlib import Path

NAME = "Increase Render Distance"
DESCRIPTION = "Increase the render distance of animals. There are two settings: when the animals spawn (get closer) or desapwn (moving away)."
FILE = "global/global_animal_types.blo"
OPTIONS = [
  { "name": "Spawn Distance", "type": int, "min": 385, "max": 1000, "default": 384, "increment": 5, "initial": 750 },
  { "name": "Despawn Distance", "type": int, "min": 420, "max": 1000, "default": 416, "increment": 5, "initial": 750 },
  { "name": "Bird Spawn Distance", "type": int, "min": 470, "max": 1000, "default": 470, "increment": 5, "initial": 750 },
  { "name": "Bird Despawn Distance", "type": int, "min": 500, "max": 1000, "default": 500, "increment": 5, "initial": 750 }
]

def format(options: dict) -> str:
  spawn_distance = int(options['spawn_distance'])
  despawn_distance = int(options['despawn_distance'])
  return f"Increase Render Distance ({spawn_distance}m, {despawn_distance}m)"

def find_prop_offset(value: float, props: List[RtpcProperty]) -> int:
  for prop in props:
    if prop.data == value:
      return prop.data_pos
  return None
    
def get_animal_props(animal_list: RtpcNode) -> RtpcNode:
  animal_props = []
  for animal in animal_list.child_table:
    animal_props.append(animal.prop_table)
  return animal_props

def open_rtpc(filename: Path) -> RtpcNode:
  with filename.open("rb") as f:
    data = rtpc_from_binary(f) 
  root = data.root_node
  return root.child_table[0]  

def process(options: dict) -> None:
  spawn_distance = options['spawn_distance']
  bird_spawn_distance = options['bird_spawn_distance']
  despawn_distance = options['despawn_distance']
  bird_despawn_distance = options['bird_despawn_distance']
  src = mods.APP_DIR_PATH / "mod/dropzone" / FILE
  animal_list = open_rtpc(src)
  animal_props = get_animal_props(animal_list)
  spawn_offsets = []
  bird_spawn_offsets = []
  despawn_offsets = []
  bird_despawn_offsets = []
  for animal in animal_props:
    bird_spawn_offset = None
    bird_despawn_offset = None
    
    spawn_offset = find_prop_offset(384.0, animal)
    if not spawn_offset:
      bird_spawn_offset = find_prop_offset(470.0, animal)
    despawn_offset = find_prop_offset(416.0, animal)
    if not despawn_offset:
      bird_despawn_offset = find_prop_offset(500.0, animal)
      
    if spawn_offset:
      spawn_offsets.append(spawn_offset)    
    if bird_spawn_offset:
      bird_spawn_offsets.append(bird_spawn_offset)
    if despawn_offset:
      despawn_offsets.append(despawn_offset)      
    if bird_despawn_offset:
      bird_despawn_offsets.append(bird_despawn_offset)      
  
  mods.update_file_at_offsets(Path(FILE), spawn_offsets, spawn_distance)
  mods.update_file_at_offsets(Path(FILE), bird_spawn_offsets, bird_spawn_distance)
  mods.update_file_at_offsets(Path(FILE), despawn_offsets, despawn_distance)
  mods.update_file_at_offsets(Path(FILE), bird_despawn_offsets, bird_despawn_distance)