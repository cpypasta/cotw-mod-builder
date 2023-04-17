import os, sys, imp, struct, shutil, json
from typing import List
from pathlib import Path
from deca.file import ArchiveFile
from deca.ff_adf import Adf
from deca.ff_sarc import FileSarc

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

def _load_mod(filename: str):
  py_mod = imp.load_source(filename.split(".")[0], str(APP_DIR_PATH / PLUGINS_FOLDER / filename))
  return py_mod

def _get_mod_filenames() -> List[str]:
  mod_filenames = []
  for mod_filename in os.listdir(APP_DIR_PATH / PLUGINS_FOLDER):
    _mod_name, file_ext = os.path.splitext(os.path.split(mod_filename)[-1])
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

def copy_file_to_mod(src_filename: str) -> None:
  dest_path = APP_DIR_PATH / "mod/dropzone" / src_filename
  if not dest_path.exists():
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    src_path = APP_DIR_PATH / "org" / src_filename
    shutil.copy(src_path, dest_path)  

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

def update_file_at_offsets(src_filename: Path, offsets: List[int], value: any, transform: str = None, format: str = None) -> None:
  dest_path = APP_DIR_PATH / "mod/dropzone" / src_filename  
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
          if transform == "multiply":
            existing_value = struct.unpack('f', fp.read(4))[0]
            value = value * existing_value
            fp.seek(offset)
          fp.write(struct.pack("f", value))
        elif isinstance(value, int):
          fp.write(struct.pack("i", value))
      fp.flush()  

def update_file_at_offset(src_filename: Path, offset: int, value: any, transform: str = None, format: str = None) -> None:
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
  adf = Adf()
  with ArchiveFile(open(GLOBAL_PATH, 'rb')) as f:
    adf.deserialize(f)
  for i, instance in enumerate(adf.table_instance_values):
    for item in instance:
      offset = item.offset + adf.table_instance[i].offset
      global_files[item.v_path.decode("utf-8")] = offset
  return global_files

def get_sarc_file_info(filename: Path) -> dict:
  bundle_files = {}
  sarc = FileSarc()
  with filename.open("rb") as fp:
    sarc.header_deserialize(fp)
    for sarc_file in sarc.entries:
      bundle_files[sarc_file.v_path.decode("utf-8")] = sarc_file.offset
  return bundle_files  

def get_player_file_info(filename: Path) -> dict:
  return get_sarc_file_info(filename)

def get_global_animal_info(filename: Path) -> dict:
  return get_sarc_file_info(filename)

def is_file_in_global(filename: str) -> bool:
  return filename in GLOBAL_FILES.keys()

def is_file_in_bundle(filename: str, lookup: dict) -> bool:
  return filename in lookup.keys()

def merge_into_file(filename: str, merge_path: str, merge_lookup: dict, delete_src: bool = False) -> None:
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

def merge_files(filenames: List[str]) -> None:
  filenames = [*set(filenames)]
  for filename in filenames:
    if is_file_in_global(filename):
      merge_into_file(filename, GLOBAL_SRC_PATH, GLOBAL_FILES, True)
    if is_file_in_bundle(filename, LOCAL_PLAYER_FILES):
      merge_into_file(filename, ELMER_MOVEMENT_LOCAL_SRC_PATH, LOCAL_PLAYER_FILES)
    if is_file_in_bundle(filename, NETWORK_PLAYER_FILES):
      merge_into_file(filename, ELMER_MOVEMENT_NETWORK_SRC_PATH, NETWORK_PLAYER_FILES)
    if is_file_in_bundle(filename, GLOBAL_ANIMAL_FILES):
      merge_into_file(filename, GLOBAL_ANIMALS_SRC_PATH, GLOBAL_ANIMAL_FILES)

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

def load_dropzone() -> None:
  steam_path = Path("C:/Program Files (x86)/Steam/steamapps/common/theHunterCotW")
  if steam_path.exists():
    steam_path = steam_path / "dropzone"
    shutil.copytree(APP_DIR_PATH / "mod/dropzone", steam_path, dirs_exist_ok=True)
  else:
    raise Exception("Could not find game path to save mods!")

def find_closest_lookup(desired_value: float, filename: str) -> int:
  root, _ext = os.path.splitext(filename)
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

# TODO: more flexible way to handle packaged files        
GLOBAL_FILES = get_global_file_info() 
LOCAL_PLAYER_FILES = get_player_file_info(ELMER_MOVEMENT_LOCAL_PATH)
NETWORK_PLAYER_FILES = get_player_file_info(ELMER_MOVEMENT_NETWORK_PATH)
GLOBAL_ANIMAL_FILES = get_global_animal_info(GLOBAL_ANIMALS_PATH)
  