from typing import List, Tuple
from modbuilder import mods
from pathlib import Path
from deca.ff_rtpc import rtpc_from_binary, RtpcNode
import PySimpleGUI as sg

NAME = "Increase Weapon Magazine"
DESCRIPTION = "Increase the magazine size of all weapons. The weapon names are stored in the configuration files, so sorry if they are a bit confusing."
FILE = "settings/hp_settings/equipment_data.bin"

def open_rtpc(filename: Path) -> RtpcNode:
  with filename.open("rb") as f:
    data = rtpc_from_binary(f) 
  root = data.root_node
  return root

def load_weapons() -> Tuple[List[str], List[dict]]:
  equipment = open_rtpc(mods.APP_DIR_PATH / "org" / FILE)
  weapons = equipment.child_table[6].child_table
  weapon_details = []
  for weapon in weapons:
    weapon_name = weapon.prop_table[4].data.decode("utf-8")
    magazine = weapon.child_table[1].prop_table[2]
    weapon_current_mag = magazine.data
    weapon_current_mag_offset = magazine.data_pos
    weapon_details.append({
      "name": f"{weapon_name} ({weapon_current_mag})",
      "current_mag": weapon_current_mag,
      "current_mag_offset": weapon_current_mag_offset
    })
  weapon_details = sorted(weapon_details, key=lambda x: x["name"])
  return ([x["name"] for x in weapon_details], weapon_details)
  
def get_option_elements() -> sg.Column:
  weapon_names, _ = load_weapons()
  ct = sg.T("Select Weapon:", p=(10,10))
  ctt = sg.T("(default magazine size showin parenthesis)", font="_ 12", p=(0,0))
  c = sg.Combo(weapon_names, k="weapon_mag_name", p=(10,10))
  st = sg.T("Select Magazine Size:", p=(10,10))
  s = sg.Slider((1, 99), 1, 1, orientation = "h", k="weapon_mag_size", p=(50,0))
  return sg.Column([[ct, ctt], [c],[st], [s]])

def add_mod(window: sg.Window, values: dict) -> dict:
  weapon_name = values["weapon_mag_name"]
  if not weapon_name:
    return {
      "invalid": "Please select weapon first"
    }
  
  weapon_names, weapon_details = load_weapons()
  weapon_mag_size = values["weapon_mag_size"]
  weapon_name_index = weapon_names.index(weapon_name)
  weapon_detail = weapon_details[weapon_name_index]
  weapon_mag_offset = weapon_detail["current_mag_offset"]
  
  return {
    "key": f"weapon_magazine_{weapon_name}",
    "invalid": None,
    "options": {
      "weapon_name": weapon_name.replace(f" ({weapon_detail['current_mag']})", ""),
      "weapon_mag_size": int(weapon_mag_size),
      "weapon_mag_offset": weapon_mag_offset
    }
  }

def format(options: dict) -> str:
  return f"{options['weapon_name']} ({options['weapon_mag_size']})"

def handle_key(mod_key: str) -> bool:
  return mod_key.startswith("weapon_magazine")
  
def process(options: dict) -> None:
  weapon_mag_size = options["weapon_mag_size"]
  weapon_mag_offset = options["weapon_mag_offset"]
  
  mods.update_file_at_offset(Path(FILE), weapon_mag_offset, weapon_mag_size)