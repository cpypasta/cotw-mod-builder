from typing import List
from modbuilder import mods
from modbuilder.adf_profile import create_u8, read_u32
from pathlib import Path
import PySimpleGUI as sg
import re, os

DEBUG = False
NAME = "Modify Ammo"
DESCRIPTION = "Modify ammo attributes. It is easy to over-adjust these settings, and then the ammo becomes unrealistic. The class changes do not show in the UI, but they do change harvest integrity."

def format_name(name: str) -> str:
  return " ".join([x.capitalize() for x in name.split("_")])

def get_relative_path(path: str) -> str:
  return os.path.relpath(path, mods.APP_DIR_PATH / "org").replace("\\", "/")

def replace_ammo_names(name: str) -> str:
  return name\
      .replace("_fn", "_flat_nose")\
      .replace("_jhp", "_jacketed_hollow_point")\
      .replace("_fnhc", "_flat_nose_hard_cast")\
      .replace("_fmj", "_full_metal_jacket")\
      .replace("_hp", "_hollow_point")\
      .replace("_nosehc", "_nose_hard_cast")\
      .replace("_sp", "_soft_point")\
      .replace("_pt", "_polymer_tip")\
      .replace("_rn", "_round_nose")\
      .replace("6_5", "6.5")\
      .replace("bh_", "")\
      .replace("jp_", "")

def load_ammo(root: Path, name_pattern: any) -> None:
  files = []
  ammo = []
  for file in root.glob("*.ammotunec"):
    name_match = name_pattern.match(file.name)
    if name_match:
      matched_name = name_match[1]
      matched_name = replace_ammo_names(matched_name)
      matched_name = format_name(matched_name)
      files.append(get_relative_path(file))
      ammo.append(matched_name)  
  return (files, ammo)

def get_ammo() -> dict:
  root_path = mods.APP_DIR_PATH / "org/editor/entities/hp_weapons/ammunition"
  ammo_name = re.compile(r'^equipment_ammo_(\w+)_\d+\.ammotunec$')
  
  bow_ammo_files, bow_ammo = load_ammo((root_path / "bows"), ammo_name)
  handgun_ammo_files, handgun_ammo = load_ammo((root_path / "handguns"), ammo_name)
  rifle_ammo_files, rifle_ammo = load_ammo((root_path / "rifles"), ammo_name)
  shotgun_ammo_files, shotgun_ammo = load_ammo((root_path / "shotguns"), ammo_name)
            
  return {
    "bow": { "files": bow_ammo_files, "ammo": bow_ammo },
    "handgun": { "files": handgun_ammo_files, "ammo": handgun_ammo },
    "rifle": { "files": rifle_ammo_files, "ammo": rifle_ammo },
    "shotgun": { "files": shotgun_ammo_files, "ammo": shotgun_ammo }
  }

def build_tab(ammo_type: str, ammo: List[str]) -> sg.Tab:
  type_key = ammo_type.lower()
  layout = [
      [sg.T("Increase Kinetic Energy Percent")],
      [sg.Slider((0, 200), 0, 2, orientation = "h", p=((50,0),(0,0)), k=f"{type_key}_kinetic_energy")],
      [sg.T("Increase Penetration Percent", p=(0, 8))],
      [sg.Slider((0, 100), 0, 2, orientation = "h", p=((50,0),(0,0)), k=f"{type_key}_penetration")],
      [sg.T("Increase Expansion Percent", p=(0, 8))],
      [sg.Slider((0, 200), 0, 2, orientation = "h", p=((50,0),(0,0)), k=f"{type_key}_expansion")],
      [sg.T("Increase Damage Percent", p=(0, 8))],
      [sg.Slider((0, 200), 0, 2, orientation = "h", p=((50,0),(0,10)), k=f"{type_key}_damage")],
      [sg.T("Increase Mass Percent", p=(0, 8))],
      [sg.Slider((0, 200), 0, 2, orientation = "h", p=((50,0),(0,10)), k=f"{type_key}_mass")],
      [sg.T("Increase Projecticle Number", p=(0, 8)) if type_key == "shotgun" else sg.T("", visible=False)],
      [sg.Slider((0, 100), 0, 2, orientation = "h", p=((50,0),(0,10)), k=f"{type_key}_projectiles") if type_key == "shotgun" else sg.T("", visible=False)],
      [sg.T("Classes", p=(0, 8)), sg.T("(select one or more)", font="_ 12")],        
      [sg.Listbox(list(range(1,10)), s=(None, 5), k=f"{type_key}_classes", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, p=((50,0),(0,20)))]             
    ]
  
  return sg.Tab(ammo_type, [
    [sg.Combo(ammo, p=((10,0),(10,10)), k=f"{type_key}_ammo")],
    [sg.Column(layout)]
  ], k=f"{ammo_type}_ammo_tab")  
        
def get_option_elements() -> sg.Column:
  ammo = get_ammo()
  
  layout = [[
    sg.TabGroup([[
      build_tab("Bow", ammo["bow"]["ammo"]),
      build_tab("Handgun", ammo["handgun"]["ammo"]),
      build_tab("Rifle", ammo["rifle"]["ammo"]),
      build_tab("Shotgun", ammo["shotgun"]["ammo"])         
    ]], k="ammo_group")
  ]]
  
  return sg.Column(layout)

def add_mod(window: sg.Window, values: dict) -> dict:
  window["ammo_group"]
  active_tab = window["ammo_group"].find_currently_active_tab_key().lower()  
  active_tab = active_tab.split("_")[0]
  ammo_name = values[f"{active_tab}_ammo"]
  
  if not ammo_name:
    return {
      "invalid": "Please select an ammo first"
    }
  
  ammo = get_ammo()
  kinetic_energy = values[f"{active_tab}_kinetic_energy"]
  penetration = values[f"{active_tab}_penetration"]
  expansion = values[f"{active_tab}_expansion"]
  damage = values[f"{active_tab}_damage"]
  mass = values[f"{active_tab}_mass"]
  projectiles = values[f"{active_tab}_projectiles"] if f"{active_tab}_projectiles" in values else 0 
  classes = values[f"{active_tab}_classes"]
  ammo_index = ammo[active_tab]["ammo"].index(ammo_name)
  file = ammo[active_tab]["files"][ammo_index]
  
  return {
    "key": f"modify_ammo_{file}",
    "invalid": None,
    "options": {
      "name": ammo_name,
      "kinetic_energy": kinetic_energy,
      "penetration": penetration,
      "expansion": expansion,
      "damage": damage,
      "mass": mass,
      "projectiles": projectiles,
      "classes": classes,
      "file": file
    }
  }

def format(options: dict) -> str:
  ammo_name = options["name"]
  kinetic_energy = int(options["kinetic_energy"])
  penetration = int(options["penetration"])
  expansion = int(options["expansion"])
  damage = int(options["damage"])
  return f"{ammo_name} ({kinetic_energy}% energy, {penetration}% penetrate, {expansion}% expand, {damage}% damage)"

def handle_key(mod_key: str) -> bool:
  return mod_key.startswith("modify_ammo")

def get_files(options: dict) -> List[str]:
  return [options["file"]]

def get_bundle_file(file: str) -> Path:
  return Path(file).parent / f"{Path(file).name.split('.')[0]}.ee"

def merge_files(files: List[str], options: dict) -> None:
  for file in files:
    bundle_file = get_bundle_file(file)
    mods.expand_into_archive(file, str(bundle_file))

def create_classes(classes: List[int]):
  result = bytearray()
  for c in classes:
    result += create_u8(c)
  return result

def process(options: dict) -> None:
  kinetic_energy = 1 + options["kinetic_energy"] / 100
  penetration = 1 - options["penetration"] / 100
  if penetration == 0:
    penetration = 0.0000001
  damage = 1 + options["damage"] / 100
  expansion_rate = 1 + options["expansion"] / 100
  max_expansion = 1 + options["expansion"] / 100
  mass = 1 + options["mass"] / 100 if "mass" in options else 0
  projectiles = int(options["projectiles"]) if "projectiles" in options else 0
  classes = options["classes"] if "classes" in options else []
  file = options["file"]
  
  mods.update_file_at_offset(file, 184, kinetic_energy, "multiply")
  mods.update_file_at_offset(file, 188, mass, "multiply")
  mods.update_file_at_offset(file, 192, penetration, "multiply")
  mods.update_file_at_offset(file, 196, damage, "multiply")
  mods.update_file_at_offset(file, 200, expansion_rate, "multiply")
  mods.update_file_at_offset(file, 204, expansion_rate, "multiply")
  mods.update_file_at_offset(file, 208, max_expansion, "multiply")
  mods.update_file_at_offset(file, 212, projectiles, "add")
  
  if len(classes) > 0:
    header_offset = 152
    data_offset = 272
    file_data = mods.get_modded_file(file).read_bytes()
    old_array_length = read_u32(file_data[header_offset+8:header_offset+12])
    new_array_length = len(classes)
    mods.insert_array_data(file, create_classes(classes), header_offset, data_offset, array_length=new_array_length, old_array_length=old_array_length)