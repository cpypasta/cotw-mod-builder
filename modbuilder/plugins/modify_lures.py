from typing import List
from modbuilder import mods
from deca.ff_rtpc import rtpc_from_binary

DEBUG=True
NAME = "Modify Lures"
DESCRIPTION = "TBD"
FILE = "settings/hp_settings/animal_interest.bin"
OPTIONS = [
    { "title": "There are no options. Just add the modification." }
]

def format(options: dict) -> str:
  return f"Modify Lures"

def process(options: dict) -> None:
    mods.update_file_at_offsets_with_values(FILE, [(21446, 300.0), (21513, 120.0)])