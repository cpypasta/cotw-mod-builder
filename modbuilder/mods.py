import os, sys, imp
from typing import List
from pathlib import Path

APP_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))

def _load_mod(filename: str):
  py_mod = imp.load_source(filename.split(".")[0], str(APP_DIR_PATH / f"mods/{filename}"))
  return py_mod

def _get_mod_filenames() -> List[str]:
  mod_filenames = []
  for mod_filename in os.listdir(APP_DIR_PATH / "mods"):
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

def get_mod(mod_file: str):
  return _load_mod(mod_file)

def list_mod_files() -> List[str]:
  return _get_mod_filenames()

def list_mods() -> List[str]:
  return [m.NAME for m in get_mods()]
  