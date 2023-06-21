import textwrap, math
import PySimpleGUI as sg
from modbuilder import __version__, logo, mods, party
from typing import List

DEFAULT_FONT = "_ 14"
MOD_LIST = mods.list_mods()
selected_mods = {}
selected_mod_names = {}

def _repack(window: sg.Window):
  mod_widget = window["mod_col"].widget
  selected_widget = window["selected_col"].widget
  mod_pack_info = mod_widget.pack_info()
  mod_pack_info.update({"expand": 0, "fill": "y"})
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
    if hasattr(mod, "OPTIONS"): # TODO: this logic is quite nested and complicated
      for mod_option in mod.OPTIONS:
        if "title" in mod_option:
          mod_details.append([sg.T(mod_option["title"])])
        else:
          key = f"{mod_key}__{_mod_name_to_key(mod_option['name'])}"
          if "style" in mod_option:
            mod_option_style = mod_option["style"]
            initial_value = mod_option["initial"] if "initial" in mod_option else mod_option["min"]
            if mod_option_style == "inline":
              if isinstance(mod_option["initial"], bool):
                t = sg.Checkbox(mod_option["name"], p=((30,10),(10,10)), k=key, default = mod_option["initial"])
                mod_details.append([t])
              else:
                t = sg.T(f"{mod_option['name']}", p=((30,10),(10,10)))
                td = sg.Input(mod_option["initial"], size=22, k=key)
                mod_details.append([t, td])
            elif mod_option_style == "list":
              t = sg.T(f"{mod_option['name']}", p=((30,10),(10,10)))
              td = sg.Combo(mod_option["initial"], k=key, p=((0,20),(10,10)))
              mod_details.append([t, td])
            elif mod_option_style == "slider":
              t = sg.T(f"{mod_option['name']}", p=((30,0),(10,10)))
              note = f" ({mod_option['note']})" if "note" in mod_option else ""
              n = sg.T(note, font="_ 12", p=(0,0))
              td = sg.Slider((mod_option["min"], mod_option["max"]), initial_value, mod_option["increment"], orientation = "h", k = key, p=((80,10),(0,10)))
              mod_details.append([t, n])
              mod_details.append([td])
            elif mod_option_style == "boolean":
              td = sg.Checkbox(mod_option["name"], initial_value, k=key)
              mod_details.append([td])
          else:          
            t = sg.T(f"{mod_option['name']}", p=(10,10))
            if "default" in mod_option:
              td = sg.T(f"(default: {mod_option['default']}, min: {mod_option['min']}, max: {mod_option['max']})", font="_ 12", p=(0,0))
            else:
              td = sg.T("")
            if "note" in mod_option:
              tn = sg.T(f"({mod_option['note']})", font="_ 12", text_color="orange", p=((10,0),(23,0)))
            else:
              tn = sg.T("")
            initial_value = mod_option["initial"] if "initial" in mod_option else mod_option["min"]
            if "min" in mod_option and "max" in mod_option and "increment" in mod_option:        
              i = sg.Slider((mod_option["min"], mod_option["max"]), initial_value, mod_option["increment"], orientation = "h", k = key, p=((50,0),(0,0)))
            else:
              i = sg.Input(initial_value, size=6, k = key, p=((50,0),(10,10)))
            mod_details.append([t, td])
            mod_details.append([i, tn])
    else:
      mod_details.append([mod.get_option_elements()])
    if (hasattr(mod, "OPTIONS") and len(mod.OPTIONS) > 3) or not hasattr(mod, "OPTIONS"):
      options.append([sg.pin(sg.Column(mod_details, k=mod_key, visible=False, vertical_scroll_only=True, scrollable=True, expand_y=True, s=(None, 400)))])
      # options.append([sg.pin(sg.Column(mod_details, k=mod_key, visible=False, vertical_scroll_only=True, scrollable=True, expand_y=True))])
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
  if mod_option == None or "min" not in mod_option: # TODO: defensive logic going on here
    return None
  min_value = mod_option["min"]
  max_value = mod_option["max"]
  mod_value = type(mod_option["initial"])(mod_value) if "initial" in mod_option else type(min_value)(mod_value)
  try:
    if mod_value >= min_value and mod_value <= max_value:
      return None
  except:
    None
  return f"Invalid Value: {mod_value} \n\nMust be between {min_value} and {max_value}"

def _enable_mod_button(window: sg.Window) -> None:
  selected_mod_size = len(window["selected_mods"].get_list_values())
  window["build_mod"].update(disabled=(selected_mod_size == 0))
  window["save"].update(disabled=(selected_mod_size == 0))

def _create_party() -> None:
  layout = [
    [sg.Image(party.value), sg.Column([
      [sg.T("Your mod has successfully been created!", font="_ 20")],
      [sg.T(mods.APP_DIR_PATH / "mod")],
      [sg.VPush()],
      [sg.Push(), sg.Button("Load to Game", k="load"), sg.Button("OK")]
    ], expand_x=True, expand_y=True)]
  ]
  
  window = sg.Window("Mod Created", layout, modal=True, icon=logo.value, font=DEFAULT_FONT)  
  
  while True:
    event, _values = window.read()
    if event == sg.WIN_CLOSED or event == "OK":
      break
    if event == "load":
      try:
        mods.load_dropzone()
        sg.PopupQuickMessage("Mods Loaded", font="_ 28", background_color="brown")
        break
      except Exception as ex:
        sg.Popup(ex, title="Error", icon=logo.value, font=DEFAULT_FONT)
  window.close()  

def _show_load_mod() -> None:
  saved_mods = mods.load_saved_mods()
  layout = [
    [sg.T("Saved Modifications", font="_ 18")],
    [sg.Listbox(saved_mods, expand_x=True, expand_y=True, k="saved_mods", enable_events=True)],
    [sg.Button("Delete", k="delete", disabled=True), sg.Push(), sg.Button("Cancel", k="cancel"), sg.Button("Merge", k="merge", disabled=True), sg.Button("Load", k="load", disabled=True)]
  ]
  window = sg.Window("Load Saved Modifications", layout, modal=True, size=(600, 300), icon=logo.value, font=DEFAULT_FONT)
  loaded_saved_mod = None
  merge = False
  
  while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "cancel":
      break    
    if event == "delete":
      delete_confirm = sg.PopupOKCancel("Are you sure you want to delete these saved modifications?", title="Delete Confirm", icon=logo.value, font=DEFAULT_FONT)
      if delete_confirm == "OK":
        mods.delete_saved_mod(values["saved_mods"][0])
        window["saved_mods"].update(mods.load_saved_mods())
        window["delete"].update(disabled=True)
        window["load"].update(disabled=True)        
        window["merge"].update(disabled=True)        
    elif event == "saved_mods":
      if len(values["saved_mods"]) == 0:
        continue
      window["delete"].update(disabled=False)
      window["load"].update(disabled=False)
      window["merge"].update(disabled=False)
    elif event == "load" or event == "merge":
      loaded_saved_mod = mods.load_saved_mod(values["saved_mods"][0])
      merge = event == "merge"
      break
  window.close()        
  return (merge, loaded_saved_mod)

def main() -> None:
  global selected_mods
  global selected_mod_names
  
  sg.theme("DarkAmber")
  sg.set_options({ "font": DEFAULT_FONT })
  
  mod_options = _get_mod_options()
  
  layout = [
    [
      sg.Image(logo.value), 
      sg.Column([
        [sg.T("Mod Builder", expand_x=True, font="_ 24")],
        [sg.T(mods.get_dropzone(), font="_ 12", k="game_path"), sg.T("(set path)", font="_ 12 underline", text_color="orange", enable_events=True, k="change_path", visible=(mods.get_dropzone() == None))],
      ]), 
      sg.Push(),
      sg.T(f"Version: {__version__}", font="_ 12", p=((0,0),(0,60)))
    ],
    [
      sg.Column([
        [sg.Frame(title="Modification", layout=[
          [sg.T("Type: ", p=((18, 10), (10,0)), font="_ 14 underline", text_color="orange"), sg.Combo(MOD_LIST, k="modification", metadata=mods.list_mod_files(), enable_events=True, p=((0, 30), (10, 0)))],
          [sg.Column(mod_options, p=(0,0), k="options", expand_y=True)],
        ], expand_y=True)],
        [sg.Button("Add Modification", k="add_mod", button_color=f"{sg.theme_element_text_color()} on brown", disabled=True, expand_x=True)]
      ], k="mod_col", expand_y=True, p=((0,0), (10,0))),
      sg.Column([
        [sg.Frame("Selected Modifications", [
          [sg.Listbox([], expand_y=True, expand_x=True, k = "selected_mods", enable_events=True)],
          [sg.Button("Save", k="save", button_color=f"{sg.theme_element_text_color()} on brown", disabled=True), sg.Button("Load", k="load", button_color=f"{sg.theme_element_text_color()} on brown"), sg.Push(), sg.Button("Remove", k="remove_mod", button_color=f"{sg.theme_element_text_color()} on brown", disabled=True)]
        ], expand_y=True, expand_x=True)],
        [sg.Button("BUILD MOD", k="build_mod", expand_x=True, disabled=True)]
      ], k="selected_col", expand_y=True, expand_x=True, p=((0,0), (10,0))),
    ],
    [
      sg.ProgressBar(100, orientation="h", k="progress", expand_x=True, s=(10,20))
    ]    
  ]

  window = sg.Window("COTW: Mod Builder", layout, resizable=True, font=DEFAULT_FONT, icon=logo.value, size=(1300, 700), finalize=True)
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

      if hasattr(mod, "add_mod"):
        result = mod.add_mod(window, values)
        is_invalid = result["invalid"]
        if not is_invalid:
          mod_options = result["options"]
          mod_key = result["key"]
      else:          
        for key, value in values.items():
          if isinstance(key, str) and mod_key in key:
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
      window["build_mod"].update(disabled=True)
      mods.clear_mod()
      mod_files = []
      step = 1
      progress_step = 95 / len(selected_mods.keys())
      for selected_mod_key, mod_options in selected_mods.items():
        mod = mods.get_mod(selected_mod_key)
        if hasattr(mod, "FILE"):
          modded_files = mods.copy_files_to_mod(mod.FILE)
        else:
          modded_files = mods.copy_all_files_to_mod(mod.get_files(mod_options))
        mod_files += modded_files
        mods.apply_mod(mod, mod_options)
        if hasattr(mod, "merge_files"): # TODO: all these possible paths should go into mods module
          mod.merge_files(modded_files, mod_options)
        step_progress = math.floor(step * progress_step)
        window["progress"].update(step_progress)
        step += 1
        
      mods.merge_files(mod_files)
      mods.package_mod()
      selected_mods = {}
      selected_mod_names = {}
      window["selected_mods"].update(_get_selected_mods(selected_mods))
      _enable_mod_button(window)
      window["remove_mod"].update(disabled=True)
      window["progress"].update(100)
      _create_party()
      window["progress"].update(0)
    elif event == "save":
      save_name = sg.PopupGetText("What name would you like use to save modifications?", title="Save Mods", font=DEFAULT_FONT, icon=logo.value)
      if save_name:
        mods.save_mods(selected_mods, save_name)
        sg.PopupQuickMessage("Modifications Saved", font="_ 28", background_color="brown")
    elif event == "load":
      merge, saved_mod = _show_load_mod()
      if saved_mod:
        selected_mods = selected_mods | saved_mod if merge else saved_mod
        selected_mod_names = {}
        for loaded_mod_key, mod_options in selected_mods.items():
            selected_mod_names[mods.get_mod(loaded_mod_key).format(mod_options)] = loaded_mod_key
        window["selected_mods"].update(_get_selected_mods(selected_mods))
        _enable_mod_button(window)     
        sg.PopupQuickMessage("Modifications Loaded", font="_ 28", background_color="brown")   
    elif event == "change_path":
      game_path = sg.PopupGetFolder("Select the game folder (folder with file theHunterCotW_F.exe)", "Game Path", icon=logo.value, font=DEFAULT_FONT)
      if game_path:
        mods.write_dropzone(game_path)
        window["game_path"].update(game_path)
        window["change_path"].update(visible=False)
    else:
      mods.delegate_event(event, window, values)
          
  window.close()

if __name__ == "__main__":
    main()