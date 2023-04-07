import textwrap
import PySimpleGUI as sg
from modbuilder import __version__, logo, mods, party
from typing import List, Tuple
from pathlib import Path

DEFAULT_FONT = "_ 14"
MOD_LIST = mods.list_mods()
selected_mods = {}
selected_mod_names = {}

def _repack(window: sg.Window):
  mod_widget = window["mod_col"].widget
  selected_widget = window["selected_col"].widget
  mod_pack_info = mod_widget.pack_info()
  mod_pack_info.update({"expand": 0})
  mod_widget.pack(**mod_pack_info, before=selected_widget)

def _mod_name_to_key(name: str) -> str:
  return mods.get_mod_key_from_name(name)

def _get_mod_options() -> List[dict]:
  possible_mods = mods.get_mods()
  options = []
  for mod in possible_mods:
    mod_details = []
    mod_key = _mod_name_to_key(mod.NAME)
    mod_details.append([sg.T("Description:", p=(10, 10), font="_ 14 underline", text_color="orange")])
    mod_details.append([sg.T(textwrap.fill(mod.DESCRIPTION, 80), p=(10,0))])
    mod_details.append([sg.T("Options:", font="_ 14 underline", text_color="orange", p=(10, 10))])
    for mod_option in mod.OPTIONS:
      key = f"{mod_key}__{_mod_name_to_key(mod_option['name'])}"
      t = sg.T(f"{mod_option['name']}", p=(10,10))
      td = sg.T(f"(default: {mod_option['default']}, min: {mod_option['min']}, max: {mod_option['max']})", font="_ 12", p=(0,0))
      initial_value = mod_option["initial"] if "initial" in mod_option else mod_option["min"]
      if "min" in mod_option and "max" in mod_option and "increment" in mod_option and mod_option["type"] == int:        
        i = sg.Slider((mod_option["min"], mod_option["max"]), initial_value, mod_option["increment"], orientation = "h", k = key, p=(50,0))
      else:
        i = sg.Input(initial_value, size=6, k = f"{mod_key}__{_mod_name_to_key(mod_option['name'])}", p=(50,10))
      mod_details.append([t, td])
      mod_details.append([i])
    if len(mod.OPTIONS) > 3:
      options.append([sg.pin(sg.Column(mod_details, k=mod_key, visible=False, vertical_scroll_only=True, scrollable=True, expand_y=True, s=(None, 400)))])
    else:
      options.append([sg.pin(sg.Column(mod_details, k=mod_key, visible=False))])
  return options

def _show_mod_options(mod_name: str, window: sg.Window) -> None:
  for mod in MOD_LIST:
    if mod == mod_name:
      window[_mod_name_to_key(mod)].update(visible=True)
    else:
      window[_mod_name_to_key(mod)].update(visible=False)

def _get_selected_mods(mods_selected: dict) -> None:
  selected_mods = []
  for mod_key, mod_options in mods_selected.items():
    selected_mods.append(mods.get_mod(mod_key).format(mod_options))
  return selected_mods

def _valid_option_value(mod_option: dict, mod_value: any) -> str:
  min_value = mod_option["min"]
  max_value = mod_option["max"]
  type_value = mod_option["type"]
  try:
    typed_value = type_value(mod_value)
    if typed_value >= min_value and typed_value <= max_value:
      return None
  except:
    None
  return f"Invalid Value: {mod_value} \n\nMust be between {min_value} and {max_value}"

def _enable_mod_button(window: sg.Window) -> None:
  selected_mod_size = len(window["selected_mods"].get_list_values())
  window["build_mod"].update(disabled=(selected_mod_size == 0))

def _create_party() -> None:
  layout = [
    [sg.Image(party.value), sg.Column([
      [sg.T("Your mod has successfully been created!", font="_ 20")],
      [sg.T(mods.APP_DIR_PATH / "mod")],
      [sg.VPush()],
      [sg.Push(), sg.Button("OK")]
    ], expand_x=True, expand_y=True)]
  ]
  
  window = sg.Window("Mod Created", layout, modal=True, icon=logo.value, font=DEFAULT_FONT)  
  
  while True:
    event, _values = window.read()
    if event == sg.WIN_CLOSED or event == "OK":
      break
  window.close()  

def main() -> None:
  global selected_mods
  
  sg.theme("DarkAmber")
  sg.set_options({ "font": DEFAULT_FONT })
  
  mod_options = _get_mod_options()
  
  layout = [
    [
      sg.Image(logo.value), 
      sg.Column([
        [sg.T("Mod Builder", expand_x=True, font="_ 24")]
      ]), 
      sg.Push(),
      sg.T(f"Version: {__version__}", font="_ 12", p=((0,0),(0,60)))
    ],
    [
      sg.Column([
        [sg.Frame(title="Modification", layout=[
          [sg.T("Type: ", p=((18, 10), (10,0)), font="_ 14 underline", text_color="orange"), sg.Combo(MOD_LIST, k="modification", metadata=mods.list_mod_files(), enable_events=True, p=((0, 30), (10, 0)))],
          [sg.Column(mod_options, p=(0,0), k="options")],
          [sg.VPush()],
          [sg.Push(), sg.Button("Add Modification", k="add_mod", button_color=f"{sg.theme_element_text_color()} on brown", disabled=True)]                    
        ], expand_y=True)]
      ], k="mod_col", expand_y=True, p=((0,0), (10,0))),
      sg.Column([
        [sg.Frame("Selected Modifications", [
          [sg.Listbox([], expand_y=True, expand_x=True, k = "selected_mods", enable_events=True)],
          [sg.Push(), sg.Button("Remove", k="remove_mod", button_color=f"{sg.theme_element_text_color()} on brown", disabled=True)]
        ], expand_y=True, expand_x=True)],
        [sg.Button("BUILD MOD", k="build_mod", expand_x=True, disabled=True)]
      ], k="selected_col", expand_y=True, expand_x=True, p=((0,0), (10,0))),
    ]    
  ]

  window = sg.Window("COTW: Mod Builder", layout, resizable=True, font=DEFAULT_FONT, icon=logo.value, size=(1200, 700), finalize=True)
  _repack(window)
  
  while True:
    event, values = window.read()    
    # print(event, values)
    if event == sg.WIN_CLOSED:
      break
    if event == "modification":
      mod_name = values["modification"]
      mod_key = _mod_name_to_key(mod_name)
      mod = mods.get_mod(mod_key)
      _show_mod_options(mod_name, window)
      window["add_mod"].update(disabled=False)
    elif event == "add_mod":
      mod_options = {}
      is_invalid = None
                      
      for key, value in values.items():
        if mod_key in key:
          option_key = key.split("__")[1]
          invalid_result = _valid_option_value(mods.get_mod_option(mod_key, option_key), value)
          if invalid_result is None:
            mod_options[option_key] = value
          else:
            is_invalid = invalid_result 
            break
      if is_invalid is None:
        selected_mods[mod_key] = mod_options
        selected_mod_names[mod.format(mod_options)] = mod_key
        window["selected_mods"].update(_get_selected_mods(selected_mods))
        _enable_mod_button(window)
      else:
        sg.PopupOK(is_invalid, icon=logo.value, title="Error", font=DEFAULT_FONT)
    elif event == "selected_mods":
      if len(values["selected_mods"]) == 0:
        continue
      selected_mod_name = values["selected_mods"][0]
      window["remove_mod"].update(disabled=False)      
    elif event == "remove_mod":
      selected_mod_key = selected_mod_names[selected_mod_name]
      del selected_mods[selected_mod_key]   
      window["selected_mods"].update(_get_selected_mods(selected_mods))   
      window["remove_mod"].update(disabled=True)
      _enable_mod_button(window)
    elif event == "build_mod":
      mods.clear_mod()
      mod_files = []
      for mod_key, mod_options in selected_mods.items():
        mod = mods.get_mod(mod_key)
        modded_files = mods.copy_files_to_mod(mod.FILE)
        mod_files += modded_files
        mods.apply_mod(mod, mod_options)
        
      mods.merge_files(mod_files)
      mods.package_mod()
      selected_mods = {}
      window["selected_mods"].update(_get_selected_mods(selected_mods))
      _enable_mod_button(window)
      window["remove_mod"].update(disabled=True)
      _create_party()
          
  window.close()

if __name__ == "__main__":
    main()