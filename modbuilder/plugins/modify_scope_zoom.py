from typing import List, Tuple
from modbuilder import mods
from pathlib import Path
import PySimpleGUI as sg
import re, os

NAME = "Modify Scope Zoom"
DESCRIPTION = "Modify the zoom range for scopes. Every zoomable scope has five zoom levels. With this mod you get to control each level of the zoom."

class Scope:
  def __init__(self, file: Path, bundle_file: Path, name: str) -> None:
    self.file = file
    self.bundle_file = bundle_file
    self.name = name
  
  def __repr__(self) -> str:
    return f"{self.name}, {self.file}, {self.bundle_file}"

def map_scope_name(folder: str) -> str:
  if folder == "rifle_scope_8-16x_50mm_01":
    return "Argus 8-16x50 Rifle"
  if folder == "rifle_scope_1-4x_24mm_01":
    return "Ascent 1-4x24 Rifle"
  if folder == "scope_muzzleloader_4-8x32_01":
    return "Galileo 4-8x32 Muzzleloader"
  if folder == "rifle_scope_night_vision_1-4x_24mm_01":
    return "GenZero 1-4x24 Night Vision Rifle"
  if folder == "rifle_scope_4-8x_32mm_01":
    return "Helios 4-8x32 Rifle"
  if folder == "rifle_scope_4-8x_42mm_01":
    return "Hyperion 4-8x42 Rifle"
  if folder == "handgun_scope_2-4x_20mm_01":
    return "Goshawk Redeye 2-4x20 Handgun"
  if folder == "rifle_scope_3_9x44mm_01":
    return "Falcon 3-9x44 Drilling Shotgun"
  if folder == "shotgun_scope_1-4x_20mm_01":
    return "Meridian 1-4x20 Shotgun"
  if folder == "crossbow_scope_1-4x_24mm_01":
    return "Hawken 1-4x24 Crossbow"
  return folder

def load_scopes() -> List[Scope]:
  scopes = []
  zoomable_scope = re.compile(r'^\w+[\-_]\d+x\w+$')
  base_path = mods.APP_DIR_PATH / "org/editor/entities/hp_weapons/sights"
  for folder in os.listdir(base_path):
    if zoomable_scope.match(folder):
      scope_file = Path("editor/entities/hp_weapons/sights") / Path(folder) / f"equipment_sight_{folder}.sighttunec"
      bundle_file = Path("editor/entities/hp_weapons/sights") / Path(folder) / f"equipment_sight_{folder}.ee"
      scopes.append(Scope(scope_file, bundle_file, map_scope_name(folder)))
  return sorted(scopes, key=lambda x: x.name)

def get_option_elements() -> sg.Column:
  scopes = load_scopes()
  return sg.Column([
    [sg.T("Scope:")],
    [sg.Combo([x.name for x in scopes], k="scope_name", p=((10,0),(0,10)))],
    [sg.T("Level 1:")],
    [sg.Slider((1, 30), 1.0, 0.5, orientation="h", k="scope_level_1", p=((10,0),(0,10)))],    
    [sg.T("Level 2:")],
    [sg.Slider((2, 30), 2.0, 0.5, orientation="h", k="scope_level_2", p=((10,0),(0,10)))],    
    [sg.T("Level 3:")],
    [sg.Slider((3, 30), 3.0, 0.5, orientation="h", k="scope_level_3", p=((10,0),(0,10)))],    
    [sg.T("Level 4:")],
    [sg.Slider((4, 30), 4.0, 0.5, orientation="h", k="scope_level_4", p=((10,0),(0,10)))],    
    [sg.T("Level 5:")],
    [sg.Slider((5, 30), 5.0, 0.5, orientation="h", k="scope_level_5", p=((10,0),(0,10)))]
  ])

def add_mod(window: sg.Window, values: dict) -> dict:
  scope_name = values["scope_name"]
  if not scope_name:
    return {
      "invalid": "Please select a scope first"
    }
  
  scopes = load_scopes()
  selected_scope = next(x for x in scopes if x.name == scope_name)
  level_1 = values["scope_level_1"]
  level_2 = values["scope_level_2"]
  level_3 = values["scope_level_3"]
  level_4 = values["scope_level_4"]
  level_5 = values["scope_level_5"]
  
  return {
    "key": f"modify_scope_{scope_name}",
    "invalid": None,
    "options": {
      "name": scope_name,
      "file": str(selected_scope.file),
      "bundle_file": str(selected_scope.bundle_file),
      "level_1": level_1,
      "level_2": level_2,
      "level_3": level_3,
      "level_4": level_4,
      "level_5": level_5
    }
  }

def format(options: dict) -> str:
  return f"{options['name']} ({options['level_1']},{options['level_2']},{options['level_3']},{options['level_4']},{options['level_5']})"

def handle_key(mod_key: str) -> bool:
  return mod_key.startswith("modify_scope")

def get_files(options: dict) -> List[str]:
  return [options["file"]]

def merge_files(files: List[str], options: dict) -> None:
  lookup = mods.get_sarc_file_info(mods.APP_DIR_PATH / "org" / options["bundle_file"])
  mods.merge_into_archive(options["file"].replace("\\", "/"), options["bundle_file"], lookup)

def process(options: dict) -> None:
  level_1 = options["level_1"]
  level_2 = options["level_2"]
  level_3 = options["level_3"]
  level_4 = options["level_4"]
  level_5 = options["level_5"]
  file = options["file"]
  
  mods.update_file_at_offset(file, 100, level_1)
  mods.update_file_at_offset(file, 104, level_2)
  mods.update_file_at_offset(file, 108, level_3)
  mods.update_file_at_offset(file, 112, level_4)
  mods.update_file_at_offset(file, 116, level_5)