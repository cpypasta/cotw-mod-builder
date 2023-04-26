from typing import List
from modbuilder import mods

NAME = "Remove Intro Logos"
DESCRIPTION = "No intro logos, which means the game will start quicker."
OPTIONS = [
  { "title": "There are no options. Just add the modification." }
]

def format(options: dict) -> str:
  return "Remove Intro Logos"

def get_files(options: dict) -> List[str]:
  return []

def merge_files(files: List[str], options: dict) -> None:
  from_base = mods.APP_DIR_PATH / "org/modded/no_intro/ui"
  to_base = mods.APP_DIR_PATH / "mod/dropzone/ui"
  mods.copy_file(from_base / "intro.gfx", to_base / "intro.gfx")
  mods.copy_file(from_base / "title.gfx", to_base / "title.gfx")

def update_values_at_offset(options: dict) -> List[dict]:
  return []