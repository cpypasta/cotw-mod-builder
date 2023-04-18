from typing import List, Tuple
from modbuilder import mods
from pathlib import Path
import PySimpleGUI as sg
import re, os, json

NAME = "Decrease Weapon Recoil"
DESCRIPTION = "Decrease the amount of recoil for all weapons. The weapon names are what is stored in the configuration files, so sorry if they are a bit confusing."

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
      build_weapon_tab("Hangun", weapons["handgun"]),
      build_weapon_tab("Rifle", weapons["rifle"]),
      build_weapon_tab("Shotgun", weapons["shotgun"])
    ]], k="weapon_recoil_group")
  ]]
  
  return sg.Column(layout)

def add_mod(window: sg.Window, values: dict) -> dict:
  active_tab = window["weapon_recoil_group"].find_currently_active_tab_key().lower() 
  active_tab = active_tab.split("_")[0]
  weapon_name = values[f"{active_tab}_weapon"]
  if not weapon_name:
    return {
      "invalid": "Please select weapon first"
    }
  
  weapons = load_weapons()[active_tab]
  recoil_percent = values[f"{active_tab}_recoil_percent"]
  weapon = None
  for w in weapons:
    if w["name"] == weapon_name:
      weapon = w
      break
  if not weapon:
    return {
      "invalid": "The weapon name could not be found"
    }    
  weapon_file = weapon["file"]
  
  return {
    "key": f"weapon_recoil_{weapon_name}",
    "invalid": None,
    "options": {
      "name": weapon_name,
      "recoil_percent": int(recoil_percent),
      "file": weapon_file
    }
  }

def format(options: dict) -> str:
  return f"{options['name']} ({options['recoil_percent']}%)"

def handle_key(mod_key: str) -> bool:
  return mod_key.startswith("weapon_recoil")

def get_files(options: dict) -> List[str]:
  return [options["file"]]

def load_archive_files(base_path: Path):
  archives = {}
  for file in base_path.glob("*.ee"):
    archive_files = list(mods.get_sarc_file_info(file).keys())
    archives[str(file)] = archive_files
  return archives

def find_archive_files(archive_files: dict, file: str) -> str:
  found_archives = []
  for archive, files in archive_files.items():
    if file in files:
      found_archives.append(os.path.relpath(archive, mods.APP_DIR_PATH / "org"))
  return found_archives

def merge_files(files: List[str]) -> None:
  base_path = mods.APP_DIR_PATH / "org" / Path(files[0]).parent.parent
  archives = load_archive_files(base_path)
  for file in files:
    bundle_files = find_archive_files(archives, file)
    for bundle_file in bundle_files:
      bundle_lookup = mods.get_sarc_file_info(mods.APP_DIR_PATH / "org" / bundle_file)
      mods.merge_into_file(file, bundle_file, bundle_lookup)

def process(options: dict) -> None:
  recoil_multiplier = 1 - options["recoil_percent"] / 100
  file = options["file"]
  
  mods.update_file_at_offsets(Path(file), [264, 268, 272, 276], recoil_multiplier, "multiply")