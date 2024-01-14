import os, sys, imp, struct, shutil, json, math
import PySimpleGUI as sg
from typing import List
from pathlib import Path
from deca.file import ArchiveFile
from deca.ff_adf import Adf
from deca.ff_sarc import FileSarc, EntrySarc
from modbuilder.adf_profile import *

APP_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
LOOKUP_PATH = APP_DIR_PATH / "org/lookups"
PLUGINS_FOLDER = "plugins"
GLOBAL_SRC_PATH = "gdc/global.gdcc"
GLOBAL_PATH = APP_DIR_PATH / "org" / GLOBAL_SRC_PATH
ELMER_MOVEMENT_LOCAL_SRC_PATH = "editor/entities/hp_characters/main_characters/local_player_character.ee"
ELMER_MOVEMENT_NETWORK_SRC_PATH = "editor/entities/hp_characters/main_characters/network_player_character.ee"
ELMER_MOVEMENT_LOCAL_PATH = APP_DIR_PATH / "org" / ELMER_MOVEMENT_LOCAL_SRC_PATH
ELMER_MOVEMENT_NETWORK_PATH = APP_DIR_PATH / "org" / ELMER_MOVEMENT_NETWORK_SRC_PATH
GLOBAL_ANIMALS_SRC_PATH = "global/global_animal_types.bl"
GLOBAL_ANIMALS_PATH = APP_DIR_PATH / "org" / GLOBAL_ANIMALS_SRC_PATH
GAME_PATH_FILE = APP_DIR_PATH / "game_path.txt"

def _load_mod(filename: str):
  py_mod = imp.load_source(filename.split(".")[0], str(APP_DIR_PATH / PLUGINS_FOLDER / filename))
  return py_mod

def _get_mod_filenames() -> List[str]:
  mod_filenames = []
  for mod_filename in os.listdir(APP_DIR_PATH / PLUGINS_FOLDER):
    _, file_ext = os.path.splitext(os.path.split(mod_filename)[-1])
    if file_ext.lower() == '.py':
      mod_filenames.append(mod_filename)
  return mod_filenames  

def get_mods() -> List:
  mod_filenames = _get_mod_filenames()
  mods = []
  for mod_filename in mod_filenames:
    loaded_mod = _load_mod(mod_filename)
    if hasattr(loaded_mod, "DEBUG") and loaded_mod.DEBUG:
      continue
    mods.append(loaded_mod)
  return mods

def get_mod_keys() -> List[str]:
  return [x.split(".")[0] for x in _get_mod_filenames()]

def get_mod(mod_key: str):
  if mod_key in get_mod_keys():
    return _load_mod(f"{mod_key}.py")
  else:
    mods = get_mods()
    for mod in mods:
      if hasattr(mod, "handle_key"):
        if mod.handle_key(mod_key):
          return mod
    return None

def delegate_event(event: str, window: sg.Window, values: dict):
  mods = get_mods()
  for mod in mods:
    if hasattr(mod, "handle_event"):
      mod.handle_event(event, window, values)
        
def get_mod_name_from_key(mod_key: str) -> str:
  return " ".join(mod_key.lower().split("_"))

def get_mod_key_from_name(mod_name: str) -> str:
  return "_".join(mod_name.lower().split(" "))

def get_mod_option(mod_key: str, option_key: str) -> dict:
  mod = get_mod(mod_key)
  for option in mod.OPTIONS:
    mod_name = get_mod_key_from_name(option["name"]) if "name" in option else None
    if mod_name == option_key:
      return option
  return None

def list_mod_files() -> List[str]:
  return _get_mod_filenames()

def list_mods() -> List[str]:
  return [m.NAME for m in get_mods()]

def clear_mod() -> None:
  path = APP_DIR_PATH / "mod"
  if path.exists():
    shutil.rmtree(path)

def copy_file(src_path: Path, dest_path: Path) -> None:
  if not dest_path.exists():
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src_path, dest_path)   

def copy_file_to_mod(src_filename: str) -> None:
  dest_path = APP_DIR_PATH / "mod/dropzone" / src_filename
  src_path = APP_DIR_PATH / "org" / src_filename
  copy_file(src_path, dest_path)  

def copy_glob_to_mod(src_filename: str) -> List[str]:
  org_basepath = APP_DIR_PATH / "org"
  files = []
  for file in list(org_basepath.glob(src_filename)):
    file = str(Path(f"{Path(src_filename).parent}/{file.name}"))
    copy_file_to_mod(file)
    files.append(file.replace("\\", "/"))
  return files

def copy_files_to_mod(src_filename: str) -> List[str]:
  if "*" in src_filename:
    return copy_glob_to_mod(src_filename)
  else:
    copy_file_to_mod(src_filename)
    return [src_filename]

def copy_all_files_to_mod(filenames: List[str]) -> List[str]:
  for filename in filenames:
    copy_file_to_mod(filename)
  return filenames

def get_org_file(src_filename: str) -> Path:
  return APP_DIR_PATH / "org" / src_filename  

def get_modded_file(src_filename: str) -> Path:
  return APP_DIR_PATH / "mod/dropzone" / src_filename  

def read_file_at_offset(src_filename: str, offset: int, format: str) -> any:
  src_path = get_org_file(src_filename)
  value_at_offset = None
  with open(src_path, "rb") as fp:
    fp.seek(offset)
    if format == "f32":
      value_at_offset = struct.unpack("f", fp.read(4))[0]
  return value_at_offset

def update_file_at_offsets(src_filename: str, offsets: List[int], value: any, transform: str = None, format: str = None) -> None:
  dest_path = get_modded_file(src_filename) 
  with open(dest_path, "r+b") as fp:
    for offset in offsets:
      fp.seek(offset)
      if format:
        if format == "sint08":
          fp.write(struct.pack("h", value))
      else:
        if isinstance(value, str):
          fp.write(struct.pack(f"{len(value)}s", value.encode("utf-8")))      
        elif isinstance(value, float):
          new_value = value
          if transform == "multiply":
            existing_value = struct.unpack('f', fp.read(4))[0]
            new_value = value * existing_value
            fp.seek(offset)
          fp.write(struct.pack("f", new_value))
        elif isinstance(value, int):
          new_value = value
          if transform == "add":
            existing_value = struct.unpack("i", fp.read(4))[0]
            new_value = value + existing_value
          elif transform == "multiply":
            existing_value = struct.unpack("i", fp.read(4))[0]
            new_value = round(value * existing_value)
          fp.seek(offset)            
          fp.write(struct.pack("i", new_value))
      fp.flush()  

def update_file_at_offsets_with_values(src_filename: str, values: list[(int, int)]) -> None:
  dest_path = get_modded_file(src_filename) 
  with open(dest_path, "r+b") as fp:
    for offset, value in values:
      fp.seek(offset)
      if isinstance(value, int):
        fp.write(struct.pack("i", value))
      elif isinstance(value, str):
        fp.write(struct.pack(f"{len(value)}s", value.encode("utf-8")))
    fp.flush()  

def update_file_at_offset(src_filename: str, offset: int, value: any, transform: str = None, format: str = None) -> None:
  update_file_at_offsets(src_filename, [offset], value, transform, format)

def apply_mod(mod: any, options: dict) -> None:
  if hasattr(mod, "update_values_at_offset"):
    updates = mod.update_values_at_offset(options)
    for update in updates:
      update_file_at_offset(Path(mod.FILE), update["offset"], update["value"], update["transform"] if "transform" in update else None)
  else:
    mod.process(options)

def get_global_file_info() -> dict:
  global_files = {}
  return global_files

def get_sarc_file_info(filename: Path, include_details: bool = False) -> dict:
  bundle_files = {}
  sarc = FileSarc()
  with filename.open("rb") as fp:
    sarc.header_deserialize(fp)
    for sarc_file in sarc.entries:
      bundle_files[sarc_file.v_path.decode("utf-8")] = sarc_file if include_details else sarc_file.offset
  return bundle_files  

def get_sarc_file_info_details(bundle_file: Path, filename: str) -> EntrySarc:
  sarc_info = get_sarc_file_info(bundle_file, True)
  for file, info in sarc_info.items():
    if file == filename:
      return info
  return None

def get_player_file_info(filename: Path) -> dict:
  return get_sarc_file_info(filename)

def get_global_animal_info(filename: Path) -> dict:
  return get_sarc_file_info(filename)

def is_file_in_global(filename: str) -> bool:
  return filename in GLOBAL_FILES.keys()

def is_file_in_bundle(filename: str, lookup: dict) -> bool:
  return filename in lookup.keys()

def merge_into_archive(filename: str, merge_path: str, merge_lookup: dict, delete_src: bool = False) -> None:
  src_path = APP_DIR_PATH / "mod/dropzone" / filename
  mod_merge_path = APP_DIR_PATH / "mod/dropzone" / merge_path
  copy_files_to_mod(merge_path)
  filename_bytes = bytearray(src_path.read_bytes())
  merge_bytes = bytearray(mod_merge_path.read_bytes())
  filename_offset = merge_lookup[filename]
  merge_bytes[filename_offset:filename_offset+len(filename_bytes)] = filename_bytes
  mod_merge_path.write_bytes(merge_bytes)
  if delete_src:
    src_path.unlink()

def recreate_archive(changed_filenames: List[str], archive_path: str) -> None:
  org_archive_path = APP_DIR_PATH / "org" / archive_path
  new_archive_path = APP_DIR_PATH / "mod/dropzone" / archive_path
  
  sarc_file = FileSarc()  
  sarc_file.header_deserialize(org_archive_path.open("rb"))
  
  org_entries = {}
  for entry in sarc_file.entries:
    file = entry.v_path.decode("utf-8")
    if file in changed_filenames:
      entry.length = (APP_DIR_PATH / "mod/dropzone" / file).stat().st_size
    else:
      org_entries[file] = entry.offset
    
  new_archive_path.parent.mkdir(parents=True, exist_ok=True)
    
  with ArchiveFile(new_archive_path.open("wb")) as new_archive:
    with org_archive_path.open("rb") as org_archive:
      sarc_file.header_serialize(new_archive)
      
      for entry in sarc_file.entries:
        data = None
        file = entry.v_path.decode("utf-8")
        if file in changed_filenames:
          data = (APP_DIR_PATH / "mod/dropzone" / file).read_bytes()
        elif entry.is_symlink:
          continue
        else:
          org_archive.seek(org_entries[file])
          data = org_archive.read(entry.length)
          
        new_archive.seek(entry.offset)
        new_archive.write(data)
  
def expand_into_archive(filename: str, merge_path: str) -> None:
  src_path = APP_DIR_PATH / "mod/dropzone" / filename
  mod_merge_path = APP_DIR_PATH / "mod/dropzone" / merge_path  
  copy_files_to_mod(merge_path)
  archive_info = get_sarc_file_info(mod_merge_path, True)
  offsets_to_update = []
  old_file_size = None
  new_file_size = len(src_path.read_bytes())
  file_offset = None
  file_length_offset = None
  prev_offset = None
  for file, sarc_entry in archive_info.items():
    if file == filename:
      file_offset = sarc_entry.offset
      file_length_offset = sarc_entry.META_entry_size_ptr
    if file_offset != None and prev_offset == file_offset:
      old_file_size = sarc_entry.offset - file_offset
    if file_offset and sarc_entry.offset > file_offset:
      offsets_to_update.append((file, sarc_entry.META_entry_offset_ptr, sarc_entry.offset + (new_file_size - old_file_size)))
    prev_offset = sarc_entry.offset
    
  merge_bytes = bytearray(mod_merge_path.read_bytes())  
  for file_to_update in offsets_to_update:
    merge_bytes[file_to_update[1]:file_to_update[1]+4] = create_u32(file_to_update[2])
 
  filename_bytes = bytearray(src_path.read_bytes())
  merge_bytes[file_length_offset:file_length_offset+4] = create_u32(new_file_size)
  del merge_bytes[file_offset:file_offset+old_file_size]
  merge_bytes[file_offset:file_offset] = filename_bytes
  mod_merge_path.write_bytes(merge_bytes)

def merge_files(filenames: List[str]) -> None:
  filenames = [*set(filenames)]
  for filename in filenames:
    if is_file_in_global(filename):
      merge_into_archive(filename, GLOBAL_SRC_PATH, GLOBAL_FILES, False)
    if is_file_in_bundle(filename, LOCAL_PLAYER_FILES):
      merge_into_archive(filename, ELMER_MOVEMENT_LOCAL_SRC_PATH, LOCAL_PLAYER_FILES)
    if is_file_in_bundle(filename, NETWORK_PLAYER_FILES):
      merge_into_archive(filename, ELMER_MOVEMENT_NETWORK_SRC_PATH, NETWORK_PLAYER_FILES)
    if is_file_in_bundle(filename, GLOBAL_ANIMAL_FILES):
      merge_into_archive(filename, GLOBAL_ANIMALS_SRC_PATH, GLOBAL_ANIMAL_FILES)

def package_mod() -> None:
  for p in list(Path(APP_DIR_PATH / "mod").glob("**/*")):
    if p.is_dir() and len(list(p.iterdir())) == 0:
      os.removedirs(p)  

def save_mods(selected_options: dict, save_name: str) -> None:
  save_path = APP_DIR_PATH / "saves"
  save_path.mkdir(parents=True, exist_ok=True)
  save_path = save_path / f"{save_name}.json"
  save_path.write_text(json.dumps(selected_options, indent=2))

def load_saved_mods() -> List[str]:
  mod_names = []
  for save in os.listdir(APP_DIR_PATH / "saves"):
    name, ext = os.path.splitext(save)
    mod_names.append(name)
  return mod_names

def delete_saved_mod(name: str) -> None:
  Path(APP_DIR_PATH / "saves"/ f"{name}.json").unlink()

def load_saved_mod(name: str) -> None:
  return json.load(Path(APP_DIR_PATH / "saves"/ f"{name}.json").open())

def read_dropzone() -> Path:
  return Path(GAME_PATH_FILE.read_text())

def write_dropzone(folder: str) -> None:
  GAME_PATH_FILE.write_text(folder)

def get_dropzone() -> Path:
  steam_path = Path("C:/Program Files (x86)/Steam/steamapps/common/theHunterCotW")
  if steam_path.exists():
    return steam_path
  elif GAME_PATH_FILE.exists():
    return read_dropzone()
  return None

def load_dropzone() -> None:
  dropzone_path = get_dropzone()
  if dropzone_path:
    dropzone_path = dropzone_path / "dropzone"
    shutil.copytree(APP_DIR_PATH / "mod/dropzone", dropzone_path, dirs_exist_ok=True)
  else:
    raise Exception("Could not find game path to save mods!")

def find_closest_lookup(desired_value: float, filename: str) -> int:
  root, _ = os.path.splitext(filename)
  numbers = json.load((LOOKUP_PATH / f"{root}.json").open())["numbers"]
  exact_match = None
  for number, cell_index in numbers.items():
    if float(number) == desired_value:
      exact_match = int(cell_index)
      break
  if exact_match:
    return exact_match
  else:
    closest_delta = 9999999
    closest_match = None
    for number, cell_index in numbers.items():
      delta = abs(float(number) - desired_value)
      if delta < closest_delta:
        closest_match = int(cell_index)
        closest_delta = delta
    return closest_match

def find_closest_lookup2(desired_value: float, numbers: dict) -> int:
  exact_match = None
  for number, cell_index in numbers.items():
    if float(number) == desired_value:
      exact_match = int(cell_index)
      break
  if exact_match:
    return exact_match
  else:
    closest_delta = 9999999
    closest_match = None
    for number, cell_index in numbers.items():
      delta = abs(float(number) - desired_value)
      if delta < closest_delta:
        closest_match = int(cell_index)
        closest_delta = delta
    return closest_match

def lookup_column(
  filename: str, 
  sheet: str, 
  col_label: str, 
  start_row: int, 
  end_row: int,
  multiplier: float
) -> (list[int], list[int]):
  root, _ = os.path.splitext(filename)
  data = json.load((LOOKUP_PATH / f"{root}.json").open())
  cells = data["sheets"][sheet]
  cell_indices = []
  for row in range(start_row, end_row + 1):
    cell_indices.append(f"{col_label}{row}")
  # print("Cells", cell_indices)
  target_cells = list(filter(lambda x: x["cell"] in cell_indices, cells))
  target_cells = sorted(target_cells, key=lambda x: x["cell"])
  # print("Target", [c["value"] for c in target_cells])
  result = []
  for c in target_cells:
    cell_index = find_closest_lookup2(c["value"] * multiplier, data["numbers"])
    result.append((c["cell_index_offset"], cell_index))
  return result

def update_non_instance_offsets(data: bytearray, profile: dict, added_size: int) -> None:
  offsets_to_update = [
    (profile["header_instance_offset"], profile["instance_header_start"]),
    (profile["header_typedef_offset"], profile["typedef_start"]),
    (profile["header_stringhash_offset"], profile["stringhash_start"]),
    (profile["header_nametable_offset"], profile["nametable_start"]),
    (profile["header_total_size_offset"], profile["total_size"]),
    (profile["instance_header_start"]+12, profile["details"]["instance_offsets"]["instances"][0]["size"])
  ]
  for offset in offsets_to_update:
    new_value = offset[1] + added_size
    if (new_value < 0):
      new_value = 0
    write_value(data, create_u32(new_value), offset[0])

def insert_array_data(file: Path, new_data: bytearray, header_offset: int, data_offset: int, array_length: int, old_array_length: int = None) -> None:
  modded_file = get_modded_file(file)
  profile = create_profile(modded_file)
  data = bytearray(modded_file.read_bytes())
  update_non_instance_offsets(data, profile, array_length-old_array_length)
  write_value(data, create_u32(array_length), header_offset+8)
  if old_array_length:
    del data[data_offset:data_offset+old_array_length]
  data[data_offset:data_offset] = new_data
  modded_file.write_bytes(data)
  
# TODO: more flexible way to handle packaged files        
GLOBAL_FILES = get_global_file_info() 
LOCAL_PLAYER_FILES = get_player_file_info(ELMER_MOVEMENT_LOCAL_PATH)
NETWORK_PLAYER_FILES = get_player_file_info(ELMER_MOVEMENT_NETWORK_PATH)
GLOBAL_ANIMAL_FILES = get_global_animal_info(GLOBAL_ANIMALS_PATH)
  