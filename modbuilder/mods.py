import os, sys, imp, struct, shutil
from typing import List
from pathlib import Path
from deca.file import ArchiveFile
from deca.ff_adf import Adf

APP_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
PLUGINS_FOLDER = "plugins"
GLOBAL_SRC_PATH = "gdc/global.gdcc"
GLOBAL_PATH = APP_DIR_PATH / "org" / GLOBAL_SRC_PATH

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
    mods.append(loaded_mod)
  return mods

def get_mod(mod_key: str):
  return _load_mod(f"{mod_key}.py")

def get_mod_name_from_key(mod_key: str) -> str:
  return " ".join(mod_key.lower().split("_"))

def get_mod_key_from_name(mod_name: str) -> str:
  return "_".join(mod_name.lower().split(" "))

def get_mod_option(mod_key: str, option_key: str) -> dict:
  mod = get_mod(mod_key)
  for option in mod.OPTIONS:
    mod_name = get_mod_key_from_name(option["name"])
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

def update_file_at_offset(src_filename: Path, offset: int, value: any) -> None:
  dest_path = APP_DIR_PATH / "mod/dropzone" / src_filename  
  with open(dest_path, "r+b") as fp:
    fp.seek(offset)
    if isinstance(value, str):
      fp.write(struct.pack(f"{len(value)}s", value.encode("utf-8")))      
    elif isinstance(value, float):
      fp.write(struct.pack("f", value))
    fp.flush()

def apply_mod(mod: any, options: dict) -> None:
  if hasattr(mod, "update_values_at_offset"):
    updates = mod.update_values_at_offset(options)
    for update in updates:
      update_file_at_offset(Path(mod.FILE), update["offset"], update["value"])
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

def is_file_in_global(filename: str) -> bool:
  return filename in GLOBAL_FILES.keys()

def merge_into_global(filename: str) -> None:
  src_path = APP_DIR_PATH / "mod/dropzone" / filename
  not_already_processed = src_path.exists()
  if not_already_processed:
    mod_global_path = APP_DIR_PATH / "mod/dropzone" / GLOBAL_SRC_PATH
    copy_files_to_mod(GLOBAL_SRC_PATH)
    mod_bytes = bytearray(src_path.read_bytes())
    global_bytes = bytearray(mod_global_path.read_bytes())
    mod_offset = GLOBAL_FILES[filename]
    global_bytes[mod_offset:mod_offset+len(mod_bytes)] = mod_bytes
    mod_global_path.write_bytes(global_bytes)
    src_path.unlink()

def merge_files(filenames: List[str]) -> None:
  for filename in filenames:
    if is_file_in_global(filename):
      merge_into_global(filename)

def package_mod() -> None:
  for p in list(Path(APP_DIR_PATH / "mod").glob("**/*")):
    if p.is_dir() and len(list(p.iterdir())) == 0:
      os.removedirs(p)  
        
GLOBAL_FILES = get_global_file_info() 
  