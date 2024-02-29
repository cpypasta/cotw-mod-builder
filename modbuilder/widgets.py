import PySimpleGUI as sg

def create_option(mod_option: dict, key: str) -> list[list]:
    mod_details = []
    if "title" in mod_option:
        mod_details.append([sg.T(mod_option["title"])])
        return mod_details
    
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
            td = sg.Slider((mod_option["min"], mod_option["max"]), initial_value, mod_option["increment"], orientation = "h", k = key, p=((80,80),(0,10)), expand_x=True)
            if "note" in mod_option:
                note = f"({mod_option['note']})"
                n = sg.T(note, font="_ 12", text_color="orange", p=((10,10),(10,10)))              
                mod_details.append([t, n])
            else:
                mod_details.append([t])
            mod_details.append([td])
        elif mod_option_style == "boolean":
            td = sg.Checkbox(mod_option["name"], initial_value, k=key)
            mod_details.append([td])
        elif mod_option_style == "listbox":
            option_name = sg.T(f"{mod_option['name']}", p=((30,0),(10,10)))
            listbox_values = mod_option["values"]
            listbox = sg.Listbox(
                listbox_values, 
                listbox_values, 
                k=key, 
                s=(None, mod_option["size"]), 
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                p=((30,30),(10,10))
            )
            mod_details.append([option_name])
            mod_details.append([listbox])
    else:
        t = sg.T(f"{mod_option['name']}", p=(10,10))
        if "default" in mod_option:
            td = sg.T(f"(default: {mod_option['default']}, min: {mod_option['min']}, max: {mod_option['max']})", font="_ 12", p=(0,0))
        else:
            td = sg.T("")
            
        initial_value = mod_option["initial"] if "initial" in mod_option else mod_option["min"]
        if "min" in mod_option and "max" in mod_option and "increment" in mod_option:        
            i = sg.Slider((mod_option["min"], mod_option["max"]), initial_value, mod_option["increment"], orientation = "h", k = key, p=((50,50),(0,0)), expand_x=True)
        else:
            i = sg.Input(initial_value, size=6, k = key, p=((50,0),(10,10)))
        if "note" in mod_option:
            tn = sg.T(f"({mod_option['note']})", font="_ 12", text_color="orange", p=((10,10),(10,10)))
            mod_details.append([t, td, tn])
        else:
            mod_details.append([t, td])
        mod_details.append([i])   
    
    return mod_details     


def valid_option_value(mod_option: dict, mod_value: any) -> str:    
    if mod_option == None or "min" not in mod_option:
        return None
    min_value = mod_option["min"]
    max_value = mod_option["max"]
    mod_type = type(mod_option["initial"]) if "initial" in mod_option else type(min_value)
    try:
        mod_value = mod_type(mod_value)
        if mod_value >= min_value and mod_value <= max_value:
            return None
    except:
        pass
    return f"Invalid Value: {mod_value} \n\nMust be between {min_value} and {max_value}"