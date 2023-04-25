from typing import List, Tuple
from modbuilder import mods
from pathlib import Path
import PySimpleGUI as sg
import re, os

NAME = "Modify Binocular Zoom"
DESCRIPTION = "Modify the zoom range for binoculars. Every zoomable binocular has five zoom levels. With this mod you get to control each level of the zoom."

class Optics:
  def __init__(self, file: Path, bundle_file: Path, name: str) -> None:
    self.file = file
    self.bundle_file = bundle_file
    self.name = name
  
  def __repr__(self) -> str:
    return f"{self.name}, {self.file}, {self.bundle_file}"

def load_binoculars() -> List[Optics]:
  base_file_path = Path("editor/entities/hp_equipment/optics/tuning")
  base_bundle_path = Path("editor/entities/hp_equipment/optics")
  return [
    Optics(base_file_path / "equipment_optics_rangefinder_01.sighttunec", base_bundle_path / "equipment_optics_rangefinder_01.ee", "Venture 5x30 Rangefinder"),
    Optics(base_file_path / "equipment_optics_rangefinder_binoculars_01.sighttunec", base_bundle_path / "equipment_optics_rangefinder_binoculars_01.ee", "Apexview 7x42 Rangefinder Binoculars"),
    Optics(base_file_path / "equipment_optics_binoculars_01.sighttunec", base_bundle_path / "equipment_optics_binoculars_01.ee", "Vantage 8x42 Binoculars"),
    Optics(base_file_path / "equipment_optics_night_vision_01.sighttunec", base_bundle_path / "equipment_optics_night_vision_01.ee", "GenZero 8x50 Night Vision"),
  ]

def get_option_elements() -> sg.Column:
  optics = load_binoculars()
  return sg.Column([
    [sg.T("Binoculars:")],
    [sg.Combo([x.name for x in optics], k="optics_name", p=((10,0),(0,10)))],
    [sg.T("Level 1:")],
    [sg.Slider((1, 30), 1.0, 0.5, orientation="h", k="optics_level_1", p=((10,0),(0,10)))],    
    [sg.T("Level 2:")],
    [sg.Slider((2, 30), 2.0, 0.5, orientation="h", k="optics_level_2", p=((10,0),(0,10)))],    
    [sg.T("Level 3:")],
    [sg.Slider((3, 30), 3.0, 0.5, orientation="h", k="optics_level_3", p=((10,0),(0,10)))],    
    [sg.T("Level 4:")],
    [sg.Slider((4, 30), 4.0, 0.5, orientation="h", k="optics_level_4", p=((10,0),(0,10)))],    
    [sg.T("Level 5:")],
    [sg.Slider((5, 30), 5.0, 0.5, orientation="h", k="optics_level_5", p=((10,0),(0,10)))]
  ])

def add_mod(window: sg.Window, values: dict) -> dict:
  optics_name = values["optics_name"]
  if not optics_name:
    return {
      "invalid": "Please select a binocular first"
    }
  
  optics = load_binoculars()
  selected_optics = next(x for x in optics if x.name == optics_name)
  level_1 = values["optics_level_1"]
  level_2 = values["optics_level_2"]
  level_3 = values["optics_level_3"]
  level_4 = values["optics_level_4"]
  level_5 = values["optics_level_5"]
  
  return {
    "key": f"modify_optics_{optics_name}",
    "invalid": None,
    "options": {
      "name": optics_name,
      "file": str(selected_optics.file),
      "bundle_file": str(selected_optics.bundle_file),
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
  return mod_key.startswith("modify_optics")

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