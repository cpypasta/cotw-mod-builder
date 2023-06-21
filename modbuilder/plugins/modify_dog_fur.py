from typing import List
from modbuilder import mods
from pathlib import Path
import PySimpleGUI as sg

DEBUG = True
NAME = "Modify Dog Fur"
DESCRIPTION = "Modify the dog furs. With this mod you can replace the existing fur with a modded one. Credit goes to PureWinter for the modded furs."
OPTIONS = [
  { "title": "Replace Original Dog Furs" },
  { "name": "Black and Tan Full Coat", "style": "list", "initial": ["Baked Issabella", "Brown and White", "Charred Brindle", "Merle", "Silver Fawn", "Wolfdog"] },
  { "name": "Red Liver Pigmented", "style": "list", "initial": ["Baked Issabella", "Brown and White", "Charred Brindle", "Merle", "Silver Fawn", "Wolfdog"] },
  { "name": "Black Tan Saddle", "style": "list", "initial": ["Baked Issabella", "Brown and White", "Charred Brindle", "Merle", "Silver Fawn", "Wolfdog"] },
  { "name": "Liver Tan Fullcoat", "style": "list", "initial": ["Baked Issabella", "Brown and White", "Charred Brindle", "Merle", "Silver Fawn", "Wolfdog"] },
  { "name": "Liver Tan Saddle", "style": "list", "initial": ["Baked Issabella", "Brown and White", "Charred Brindle", "Merle", "Silver Fawn", "Wolfdog"] },
  { "name": "Red and Black Pigmented", "style": "list", "initial": ["Baked Issabella", "Brown and White", "Charred Brindle", "Merle", "Silver Fawn", "Wolfdog"] },
]

def format(options: dict) -> str:
  return f"Modify Dog Furs"

def get_files(options: dict) -> List[str]:
  return []

def merge_files(files: List[str], options: dict) -> None:
  red_and_black_pigmented = "bloodhound_redblackpigmented_dif.ddsc"  
  black_and_tan_full_coat = "bloodhound_blacktan_dif.ddsc"
  black_tan_saddle = "bloodhound_common_dif.ddsc"
  liver_tan_saddle = "bloodhound_livertansaddle_dif.ddsc"
  red_liver_pigmented = "bloodhound_redliverpigmented_dif.ddsc"
  liver_tan_fullcoat = "bloodhound_livertanfullcoat_dif.ddsc"
  org_files = [black_and_tan_full_coat, red_liver_pigmented, black_tan_saddle, liver_tan_fullcoat, liver_tan_saddle, red_and_black_pigmented]
  
  black_and_tan_full_coat_choice = options["black_and_tan_full_coat"]
  red_liver_pigmented_choice = options["red_liver_pigmented"]
  black_tan_saddle_choice = options["black_tan_saddle"]
  liver_tan_fullcoat_choice = options["liver_tan_fullcoat"]
  liver_tan_saddle_choice = options["liver_tan_saddle"]
  red_and_black_pigmented_choice = options["red_and_black_pigmented"]
  choices = [black_and_tan_full_coat_choice, red_liver_pigmented_choice, black_tan_saddle_choice, liver_tan_fullcoat_choice, liver_tan_saddle_choice, red_and_black_pigmented_choice]
  
  base_path = "models/hp_characters/animals/bloodhound/color_variations"         
  mod_base_path = "modded/dog_color_variations"
  female_archive_path = "editor/entities/hp_characters/dogs/bloodhound/bloodhound_female.ee"
  male_archive_path = "editor/entities/hp_characters/dogs/bloodhound/bloodhound_male.ee" 
  files_to_merge = []
  for i, choice in enumerate(choices):
    if choice != "":
      dest_filename = org_files[i]
      dest_path =  f"{base_path}/{dest_filename}"
      src_filename = f"{choice.lower().replace(' ', '_')}.ddsc"
      print(src_filename, "to", dest_filename)
      mods.copy_file(mods.APP_DIR_PATH / "org" / mod_base_path / src_filename, mods.APP_DIR_PATH / "mod/dropzone" / dest_path)
      files_to_merge.append(dest_path)
      
  mods.recreate_archive(files_to_merge, female_archive_path)
  mods.recreate_archive(files_to_merge, male_archive_path)

def process(options: dict) -> None:
  None