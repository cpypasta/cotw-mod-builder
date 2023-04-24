from typing import List, Tuple
from modbuilder import mods
from pathlib import Path
import PySimpleGUI as sg
import re, os

NAME = "Modify Scope"
DESCRIPTION = "Modify the range for scopes."

def format_name(name: str) -> str:
  return " ".join([x.capitalize() for x in name.split("_")])

def get_relative_path(path: str) -> str:
  return os.path.relpath(path, mods.APP_DIR_PATH / "org").replace("\\", "/")

def load_weapon_type(root: Path, name_pattern: any) -> List[dict]:
  weapons = []
  for file in root.glob("*.wtunec"):
    name_match = name_pattern.match(file.name)
    if name_match:
      matched_name = name_match[1]
      matched_name = format_name(matched_name)
      file = get_relative_path(file)
      weapons.append({ "name": matched_name, "file": file })  
  return weapons

def load_weapons() -> Tuple[List[str], List[dict]]:
  base_path = mods.APP_DIR_PATH / "org/editor/entities/hp_weapons"
  weapon_name_pattern = re.compile(r'^weapon_([\w\d]+).wtunec$')
  
  bows = load_weapon_type(base_path / "weapon_bows_01/tuning", weapon_name_pattern)
  handguns = load_weapon_type(base_path / "weapon_handguns_01/tuning", weapon_name_pattern)
  rifles = load_weapon_type(base_path / "weapon_rifles_01/tuning", weapon_name_pattern)
  shotguns = load_weapon_type(base_path / "weapon_shotguns_01/tuning", weapon_name_pattern)
  
  return {
    "bow": bows,
    "handgun": handguns,
    "rifle": rifles,
    "shotgun": shotguns
  }

def build_weapon_tab(weapon_type: str, weapons: List[dict]) -> sg.Tab:
  type_key = weapon_type.lower()
  weapon_names = [x["name"] for x in weapons]
  return sg.Tab(weapon_type, [
    [sg.Combo(weapon_names, p=((10,0),(20,10)), k=f"{type_key}_weapon")],
    [sg.T("Decrease Recoil Percentage:")],
    [sg.Slider((0,100), 0, 2, orientation="h", p=((50,0),(0,20)), k=f"{type_key}_recoil_percent")]
  ], k=f"{weapon_type}_recoil_tab")

def get_option_elements() -> sg.Column:
  weapons = load_weapons()
  
  layout = [[
    sg.TabGroup([[
      build_weapon_tab("Bow", weapons["bow"]),
      build_weapon_tab("Handgun", weapons["handgun"]),
      build_weapon_tab("Rifle", weapons["rifle"]),
      build_weapon_tab("Shotgun", weapons["shotgun"])
    ]], k="weapon_recoil_group")
  ]]
  
  return sg.Column(layout)

def add_mod(window: sg.Window, values: dict) -> dict:
  None

def format(options: dict) -> str:
  return f"{options['name']}"

def handle_key(mod_key: str) -> bool:
  return mod_key.startswith("scopes")

def merge_files(files: List[str]) -> None:
  None

def process(options: dict) -> None:
  None