from modbuilder import mods
from pathlib import Path
import PySimpleGUI as sg

DEBUG = True
NAME = "Modify Animal Aggression"
DESCRIPTION = "Allows you to customize the aggression of animal species."
FILE = "settings/hp_settings/animal_senses.bin"

animals = {
  "wild_boar": "F",
  "eu_bison": "H",
  "cape_buffalo": "X",
  "warthog": "Y",
  "water_buffalo": "AL",
  "plains_bision": "AR",
  "feral_pig": "BF",
  "collared_peccary": "BK"
}

def get_option_elements() -> sg.Column:
  None

def add_mod(window: sg.Window, values: dict) -> dict:
  None

def format(options: dict) -> str:
  None

def handle_key(mod_key: str) -> bool:
  None

def get_files(options: dict) -> list[str]:
  None

def merge_files(files: list[str], options: dict) -> None:
  None

def process(options: dict) -> None:
  None