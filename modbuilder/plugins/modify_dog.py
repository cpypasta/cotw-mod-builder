from typing import List
from modbuilder import mods

DEBUG = True
NAME = "Modify Dog"
DESCRIPTION = "This will allow you to unlock all the traits for your dog and/or increase the XP your dog earns. Note, the UI will show all traits as green and you can unlock any trait up to the dog's level. Even if it is green, you still have to press 'learn' to learn the trait. Even after pressing 'learn', the trait will still show the 'learn' button after six have been learned. I know this experience is not ideal, but it is a limitation of the game."
DOG_FILE = "settings/hp_settings/dog_stats.bin"
OPTIONS = [
  { "name": "Allow All Traits to be Learned", "style": "boolean", "initial": False },
  { "name": "Dog XP Multiplier", "min": 1, "max": 20, "default": 1, "increment": 1 },
]

def format(options: dict) -> str:
  traits = options["allow_all_traits_to_be_learned"]
  xp = int(options["dog_xp_multiplier"])
  both = traits and xp != 1
  return f"Modify Dog ({str(xp) + 'x' if xp != 1 else ''}{', ' if both else ''}{'unlock traits' if traits else ''})"

def merge_files(files: List[str], options: dict) -> None:
  traits = options["allow_all_traits_to_be_learned"]
  if traits:
    from_base = mods.APP_DIR_PATH / "org/modded/dog_traits/ui"
    to_base = mods.APP_DIR_PATH / "mod/dropzone/ui"
    mods.copy_file(from_base / "dog_status.gfx", to_base / "dog_status.gfx")

def get_files(options: dict) -> List[str]:
  xp = int(options["dog_xp_multiplier"]) 
  return [DOG_FILE] if xp > 1 else []

def process(options: dict) -> None:
  xp = int(options["dog_xp_multiplier"])  
  
  if xp == 1:
    return None
  
  base_passive = 0.05000000074505806
  base_sit = 5.0
  base_heel = 5.0
  base_detect = 25.0
  base_track = 25.0
  base_retrieve = 25.0
  new_passive_cell = mods.find_closest_lookup(base_passive * xp, DOG_FILE)
  new_sit_cell = mods.find_closest_lookup(base_sit * xp, DOG_FILE)
  new_heel_cell = mods.find_closest_lookup(base_heel * xp, DOG_FILE)
  new_detect_cell = mods.find_closest_lookup(base_detect * xp, DOG_FILE)
  new_track_cell = mods.find_closest_lookup(base_track * xp, DOG_FILE)
  new_retrieve_cell = mods.find_closest_lookup(base_retrieve * xp, DOG_FILE)
  
  updates = [
    {
      "offset": 11804,
      "value": new_passive_cell
    },
    {
      "offset": 11960,
      "value": new_sit_cell
    },
    {
      "offset": 12116,
      "value": new_heel_cell
    },
    {
      "offset": 12428,
      "value": new_detect_cell
    },
    {
      "offset": 12584,
      "value": new_track_cell
    },
    {
      "offset": 12740,
      "value": new_retrieve_cell
    },
  ]
  
  for update in updates:
    mods.update_file_at_offset(DOG_FILE, update["offset"], update["value"])