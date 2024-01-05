from typing import Tuple, List
from deca.ff_rtpc import rtpc_from_binary, RtpcProperty, RtpcNode
from pathlib import Path
from modbuilder import mods
from functools import reduce

DEBUG = False
NAME = "Increase Reserve Population"
DESCRIPTION = "Increases the number of animals that get populated when loading a reserve for the first time. If you have already played a reserve, you need to delete the old pouplation file first before you will see an increase in animals."
FILE = "settings/hp_settings/reserve_*.bin"
OPTIONS = [
  { "name": "Population Multiplier", "min": 2, "max": 8, "default": 1, "increment": 1 }
]
  
def format(options: dict) -> str:
  multiply = int(options["population_multiplier"])
  return f"Increase Reserve Population ({multiply}x)"

class ReserveValue:
  def __init__(self, value: int, offset: int) -> None:
    self.value = value
    self.offset = offset
    
  def __repr__(self):
    return f"{self.value:} ({self.offset})"
  
def _save_file(filename: str, data: bytearray) -> None:
    base_path = mods.APP_DIR_PATH / "mod/dropzone/settings/hp_settings"
    base_path.mkdir(exist_ok=True, parents=True)
    (base_path / filename).write_bytes(data) 

def _all_non_zero_props(props: List[RtpcProperty]) -> List[ReserveValue]:
  offsets = []
  for prop in props:
    if prop.data != 0:
      offsets.append(ReserveValue(prop.data, prop.data_pos))
  return offsets

def _big_props(props: List[RtpcProperty]) -> List[ReserveValue]:
  offsets = []
  first = props[-4]
  second = props[-1]
  if first.data != 0:
    offsets.append(ReserveValue(first.data, first.data_pos))
  if second.data != 0:
    offsets.append(ReserveValue(second.data, second.data_pos))
  return offsets

def _update_uint(data: bytearray, offset: int, new_value: int) -> None:
    value_bytes = new_value.to_bytes(4, byteorder='little')
    for i in range(0, len(value_bytes)):
        data[offset + i] = value_bytes[i]

def update_reserve_population(root: RtpcNode, f_bytes: bytearray, multiply: int, debug: bool = False) -> None:
  config_children = root.child_table[0].child_table

  offsets_to_change = []
  for child in config_children:
    first_child = child.child_table[0]
    second_child = child.child_table[1]

    pattern_one = first_child.prop_count == 4
    pattern_two = first_child.prop_count == 0 
    if pattern_one:
      pattern_one_one = second_child.prop_count == 0
      if pattern_one_one:
        if first_child.child_count == 0:
          result = _all_non_zero_props(first_child.prop_table)
          offsets_to_change.append(result)
        second_child_children = second_child.child_table
        for child in second_child_children:     
          result = _big_props(child.prop_table)
          offsets_to_change.append(result)    
      else:                    
        result = _all_non_zero_props(first_child.prop_table)
        offsets_to_change.append(result)
    elif pattern_two:
        first_child_children = first_child.child_table
        for child in first_child_children:
          result = _big_props(child.prop_table)          
          offsets_to_change.append(_big_props(child.prop_table))
       
  reserve_values = reduce(lambda a, b: a + b, offsets_to_change)
  try:
    for reserve_value in reserve_values:
      _update_uint(f_bytes, reserve_value.offset, reserve_value.value * multiply)
  except Exception as ex:
     print(f"received error: {ex}")       

def _open_reserve(filename: Path) -> Tuple[RtpcNode, bytearray]:
  with(filename.open("rb") as f):
    data = rtpc_from_binary(f) 
  f_bytes = bytearray(filename.read_bytes())
  return (data.root_node, f_bytes)

def update_all_populations(source: Path, multiply: int) -> None:
  for file in list(source.glob("reserve_*.bin")):
    root, data = _open_reserve(file)
    update_reserve_population(root, data, multiply)
    _save_file(file, data)

def process(options: dict) -> None:
  multiply = int(options["population_multiplier"])
  update_all_populations(mods.APP_DIR_PATH / "mod/dropzone/settings/hp_settings", multiply)