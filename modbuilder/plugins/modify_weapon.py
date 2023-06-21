from typing import List, Tuple
from modbuilder import mods
from pathlib import Path
import PySimpleGUI as sg
import re, os

#verified
NAME = "Modify Weapon"
DESCRIPTION = "Modify weapon recoil and zeroing settings. Be careful adjusting the zeroing settings, since it may require changing ammo kinetic energy also to work well."

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
  weapon_name_pattern = re.compile(r'^weapon_([\w\d\-]+).wtunec$')
  
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
    [sg.Combo(weapon_names, p=((10,0),(20,10)), k=f"{type_key}_weapon", enable_events=True)],
    [sg.T("Decrease Recoil Percentage:")],
    [sg.Slider((0,100), 0, 2, orientation="h", p=((50,0),(0,20)), k=f"{type_key}_recoil_percent")],
    [sg.T("Zeroing Settings:"), sg.T("(distance, angle)", font="_ 12")],
    [sg.T("Level 1: ", p=((20,0),(10,10))), sg.Input("", size=4, p=((10,0),(0,0)), k=f"{type_key}_level_1_distance"), sg.Input("", p=((10,10),(0,0)), k=f"{type_key}_level_1_angle")],
    [sg.T("Level 2: ", p=((20,0),(10,10))), sg.Input("", size=4, p=((10,0),(0,0)), k=f"{type_key}_level_2_distance"), sg.Input("", p=((10,10),(0,0)), k=f"{type_key}_level_2_angle")],
    [sg.T("Level 3: ", p=((20,0),(10,10))), sg.Input("", size=4, p=((10,0),(0,0)), k=f"{type_key}_level_3_distance"), sg.Input("", p=((10,10),(0,0)), k=f"{type_key}_level_3_angle")],
    [sg.T("")]
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

class WeaponZeroing:
  def __init__(self, one_distance: float, one_angle: float, two_distance: float, two_angle: float, three_distance: float, three_angle: float) -> None:
    self.one_distance = one_distance
    self.one_angle = one_angle
    self.two_distance = two_distance
    self.two_angle = two_angle
    self.three_distance = three_distance
    self.three_angle = three_angle
  

def load_weapon_zeroing(file: str) -> WeaponZeroing:
  two_distance = mods.read_file_at_offset(file, 384, "f32")
  if two_distance == 0:
    return None
  two_angle = mods.read_file_at_offset(file, 388, "f32")
  one_distance = mods.read_file_at_offset(file, 432, "f32")
  one_angle = mods.read_file_at_offset(file, 436, "f32")
  three_distance = mods.read_file_at_offset(file, 480, "f32")
  three_angle = mods.read_file_at_offset(file, 484, "f32")
  return WeaponZeroing(one_distance, one_angle, two_distance, two_angle, three_distance, three_angle)

def zeroing_disabled(disable: bool, type_key: str, window: sg.Window) -> None:
  window[f"{type_key}_level_1_distance"].update("0", disabled=disable)
  window[f"{type_key}_level_1_angle"].update("0", disabled=disable)
  window[f"{type_key}_level_2_distance"].update("0", disabled=disable)
  window[f"{type_key}_level_2_angle"].update("0", disabled=disable)
  window[f"{type_key}_level_3_distance"].update("0", disabled=disable)
  window[f"{type_key}_level_3_angle"].update("0", disabled=disable)

def handle_event(event: str, window: sg.Window, values: dict) -> None:
  if event.endswith("_weapon"):
    type_key = event.split("_")[0]
    weapons = load_weapons()[type_key]
    weapon_name = values[event]
    weapon = next(w for w in weapons if w["name"] == weapon_name)
    weapon_zeroing = load_weapon_zeroing(weapon["file"])
    if weapon_zeroing:
      zeroing_disabled(False, type_key, window)
      window[f"{type_key}_level_1_distance"].update(int(weapon_zeroing.one_distance))
      window[f"{type_key}_level_1_angle"].update(weapon_zeroing.one_angle)
      window[f"{type_key}_level_2_distance"].update(int(weapon_zeroing.two_distance))
      window[f"{type_key}_level_2_angle"].update(weapon_zeroing.two_angle)
      window[f"{type_key}_level_3_distance"].update(int(weapon_zeroing.three_distance))
      window[f"{type_key}_level_3_angle"].update(weapon_zeroing.three_angle)
    else:
      zeroing_disabled(True, type_key, window)

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
  one_distance = float(values[f"{active_tab}_level_1_distance"])
  one_angle = float(values[f"{active_tab}_level_1_angle"])
  two_distance = float(values[f"{active_tab}_level_2_distance"])
  two_angle = float(values[f"{active_tab}_level_2_angle"])
  three_distance = float(values[f"{active_tab}_level_3_distance"])
  three_angle = float(values[f"{active_tab}_level_3_angle"])
  weapon = next(w for w in weapons if w["name"] == weapon_name) 
  weapon_file = weapon["file"]
  
  return {
    "key": f"weapon_recoil_{weapon_name}", # TODO: remove old key eventually
    "invalid": None,
    "options": {
      "name": weapon_name,
      "file": weapon_file,
      "recoil_percent": int(recoil_percent),
      "one_distance": one_distance,
      "one_angle": one_angle,
      "two_distance": two_distance,
      "two_angle": two_angle,
      "three_distance": three_distance,
      "three_angle": three_angle
    }
  }

def format(options: dict) -> str:
  return f"{options['name']} ({options['recoil_percent']}%{' w/ zeroing' if 'one_distance' in options and options['one_distance'] != 0 else ''})"

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

def merge_files(files: List[str], options: dict) -> None:
  base_path = mods.APP_DIR_PATH / "org" / Path(files[0]).parent.parent
  archives = load_archive_files(base_path)
  for file in files:
    bundle_files = find_archive_files(archives, file)
    for bundle_file in bundle_files:
      bundle_lookup = mods.get_sarc_file_info(mods.APP_DIR_PATH / "org" / bundle_file)
      mods.merge_into_archive(file, bundle_file, bundle_lookup)

def process(options: dict) -> None:
  recoil_multiplier = 1 - options["recoil_percent"] / 100
  file = options["file"]
  
  mods.update_file_at_offsets(Path(file), [264, 268, 272, 276], recoil_multiplier, "multiply")
  
  if "one_distance" in options:
    one_distance = options["one_distance"]  
    one_angle = options["one_angle"]  
    two_distance = options["two_distance"]  
    two_angle = options["two_angle"]  
    three_distance = options["three_distance"]  
    three_angle = options["three_angle"]  
    
    mods.update_file_at_offset(Path(file), 384, two_distance)
    mods.update_file_at_offset(Path(file), 388, two_angle)
    mods.update_file_at_offset(Path(file), 432, one_distance)
    mods.update_file_at_offset(Path(file), 436, one_angle)
    mods.update_file_at_offset(Path(file), 480, three_distance)
    mods.update_file_at_offset(Path(file), 484, three_angle)