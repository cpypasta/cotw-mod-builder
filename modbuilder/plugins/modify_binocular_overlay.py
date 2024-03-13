from typing import List
from modbuilder import mods

DEBUG=False
NAME = "Modify Binocular Overlay"
DESCRIPTION = "Modify the binocular overlay."
OPTIONS = [
  { "name": "Binoculars Overlay", "style": "list", "initial": ["pill", "wide"] }
]

def format(options: dict) -> str:
  return f"Modify Binocular Overlay ({options['binoculars_overlay']})"

def get_files(options: dict) -> List[str]:
  return []

def merge_files(files: List[str], options: dict) -> None:
  from_base = mods.APP_DIR_PATH / "org/modded/binocular_overlay"
  to_base = mods.APP_DIR_PATH / "mod/dropzone/ui"
  overlay = options['binoculars_overlay']
  try:
    mods.copy_file(from_base / f"{overlay}.ddsc", to_base / "hud_i45a.ddsc")
  except:
    print(f"Error: Could not copy {overlay}.ddsc")
    pass

def update_values_at_offset(options: dict) -> List[dict]:
  return []