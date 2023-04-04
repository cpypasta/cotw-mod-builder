import textwrap
import PySimpleGUI as sg
from modbuilder import __version__, logo, mods

DEFAULT_FONT = "_ 14"

def main() -> None:
  sg.theme("DarkAmber")
  
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
          [sg.T("Type: ", p=(10, 10), font="_ 14 underline"), sg.Combo(mods.list_mods(), k="modification", metadata=mods.list_mod_files(), enable_events=True)],
          [sg.Column([
            [sg.T("Description:", p=(10, 10), font="_ 14 underline")],
            [sg.T("", k="description", p=(10,0), s=(65, None))],
            [sg.T("Options:", font="_ 14 underline", p=(10, 10))],
            [sg.T("Pressure Radius: ", p=(10,0)), sg.Input("20", size=4)],          
            [sg.T("Reduce Pressure Amount (percent): ", p=(10,0)), sg.Input("50", size=4)],          
            [sg.T("Reduce Structure Pressure Amount (percent): ", p=(10,0)), sg.Input("10", size=4)]
          ], p=(0,0), expand_y=True)],
          [sg.VPush()],
          [sg.Push(), sg.Button("Reset", button_color=f"{sg.theme_element_text_color()} on brown"), sg.Button("Add Modification", button_color=f"{sg.theme_element_text_color()} on brown")]                    
        ], expand_y=True, expand_x=True, p=((0,0), (10,0)))]
      ], expand_y=True, expand_x=True),
      sg.Column([
        [sg.Frame("Selected Modifications", [
          [sg.Listbox(["Harvest Cash (x3)", "Harvest XP (x1)", "Reduce Hunting Pressure (50%)"], expand_y=True, expand_x=True)],
          [sg.Push(), sg.Button("Remove", button_color=f"{sg.theme_element_text_color()} on brown"), sg.Button("Edit", button_color=f"{sg.theme_element_text_color()} on brown")]
        ], expand_y=True, expand_x=True)],
        [sg.Button("BUILD MOD", expand_x=True)]
      ], expand_y=True, expand_x=True, p=((0,0), (10,0))),
    ]
  ]

  window = sg.Window("COTW: Mod Builder", layout, resizable=True, font=DEFAULT_FONT, icon=logo.value, size=(1300, 600))
  
  while True:
    event, values = window.read()    
    # print(event, values)
    if event == sg.WIN_CLOSED:
      break
    if event == "modification":
      selected_mod = values["modification"]
      mod_values = window["modification"].Values
      mod_metadata = window["modification"].metadata
      mod = mods.get_mod(mod_metadata[mod_values.index(selected_mod)])
      window["description"].update(textwrap.fill(mod.DESCRIPTION, 80))

  window.close()

if __name__ == "__main__":
    main()