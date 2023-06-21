from typing import List, Tuple
from modbuilder import mods
from pathlib import Path
from deca.ff_rtpc import rtpc_from_binary, RtpcNode
import PySimpleGUI as sg
import re

#verification
NAME = "Modify Store"
DESCRIPTION = "Modify the store prices. I would discourage you from adding individual and bulk modifications for the same category at the same time."
EQUIPMENT_FILE = "settings/hp_settings/equipment_data.bin"
DEBUG = False

class StoreItem:
  def __init__(self, type: str, name: str, price: int, price_offset: int) -> None:
    self.type = type
    self.name = name
    self.price = price
    self.price_offset = price_offset
  
  def __repr__(self) -> str:
    return f"{self.type}, {self.name} ({self.price}, {self.price_offset})"

def open_rtpc(filename: Path) -> RtpcNode:
  with filename.open("rb") as f:
    data = rtpc_from_binary(f) 
  root = data.root_node
  return root

def load_price_node(items: List[RtpcNode], type: str, name_offset: int = 4, price_offset: int = 7, name_handle: callable = None, price_handle: callable = None):
  prices = []
  for item in items:
    if name_handle:
      name = name_handle(item)
    else:
      try:
        name = item.prop_table[name_offset].data.decode("utf-8")
      except:
        name = "unknown"
    if price_handle:
      price, price_offset_value = price_handle(item)
    else:
      price_item = item.prop_table[price_offset]
      price = price_item.data
      price_offset_value = price_item.data_pos
    prices.append(StoreItem(type, f"{name} (id: {price_offset_value})", price, price_offset_value))
  return sorted(prices, key=lambda x: x.name)

def handle_atv_name(item: RtpcNode) -> str:
  name = item.prop_table[9].data.decode("utf-8")
  parts = name.split("\\")[-1].replace("vehicle_atv_", "").replace(".ddsc", "").split("_")
  return " ".join([x.capitalize() for x in parts])

def handle_lure_name(item: RtpcNode) -> str:
  if isinstance(item.prop_table[1].data, bytes):
    return item.prop_table[1].data.decode("utf-8")
  elif isinstance(item.prop_table[4].data, bytes):
    return item.prop_table[4].data.decode("utf-8")
  return "Unknown Lure"

def  handle_lure_price(item: RtpcNode) -> Tuple[int,int]:
  if isinstance(item.prop_table[1].data, bytes) and "caller" in item.prop_table[1].data.decode("Utf-8").lower():
    return (item.prop_table[0].data, item.prop_table[0].data_pos)
  else:
    return (item.prop_table[7].data, item.prop_table[7].data_pos)

def handle_skin_name(item: RtpcNode) -> str:
  if isinstance(item.prop_table[9].data, bytes):
    parts = item.prop_table[9].data.decode("utf-8").split("\\")
    map = " ".join([x.capitalize() for x in parts[-2].split("_")])
    name = parts[-1].replace(".ddsc", "").replace("_dif", "")
    return f"{map} {name}"
  return "Unknown Skin"

def handle_misc_name(item: RtpcNode) -> str:
  return re.sub(r'\([\w\s\-\'\./]+\)$', "", item.prop_table[4].data.decode("utf-8"))

def load_equipement_prices() -> dict:
  equipment = open_rtpc(mods.APP_DIR_PATH / "org" / EQUIPMENT_FILE)
  ammo_items = equipment.child_table[0].child_table
  misc_items = equipment.child_table[1].child_table
  sights_items = equipment.child_table[2].child_table
  optic_items = equipment.child_table[3].child_table
  atv_items = equipment.child_table[4].child_table
  skin_items = equipment.child_table[5].child_table
  weapon_items = equipment.child_table[6].child_table
  portable_items = equipment.child_table[7].child_table
  lures_items = equipment.child_table[8].child_table
  
  return {
    "ammo": load_price_node(ammo_items, "Ammo", name_offset=1, price_offset=0),
    "misc": load_price_node(misc_items, "Misc", name_handle=handle_misc_name),
    "sight": load_price_node(sights_items, "Sight", name_offset=1, price_offset=0),
    "optic": load_price_node(optic_items, "Optic"),
    "atv": load_price_node(atv_items, "ATV", name_handle=handle_atv_name),
    "skin": load_price_node(skin_items, "Skin", name_handle=handle_skin_name),
    "weapon": load_price_node(weapon_items, "Weapon", price_offset=8, name_handle=handle_misc_name),
    "structure": load_price_node(portable_items, "Structure"),
    "lure": load_price_node(lures_items, "Lure", name_handle=handle_lure_name, price_handle=handle_lure_price)
  }

def build_tab(type: str, items: List[StoreItem]) -> sg.Tab:
  type_key = type.lower()
  layout = [
    [sg.T("Individual:", p=((10,0),(20,0)), text_color="orange")],
    [sg.T("Item", p=((30,7),(10,0))), sg.Combo([x.name for x in items], metadata=items, k=f"{type_key}_item_name", p=((10,10),(10,0)), enable_events=True)],
    [sg.T("Price", p=((30,0),(10,0))), sg.Input("", size=10, p=((10,0),(10,0)), k=f"{type_key}_item_price")],
    [sg.T("Bulk:", p=((10,0),(20,0)), text_color="orange"), sg.T("(applies to all items in this category)", font="_ 12", p=((0,0),(20,0)))],
    [sg.T("Change Free to Price", p=((30,0),(10,0)))],
    [sg.Input("", size=10, p=((60,0),(10,0)), k=f"{type_key}_free_price")], 
    [sg.T("Discount Percent", p=((30,0),(10,0)))],
    [sg.Slider((0,100), 0, 1, orientation="h", p=((60,0),(10,20)), k=f"{type_key}_discount")],
  ]
  
  return sg.Tab(type, layout, k=f"{type_key}_store_tab")

def get_option_elements() -> sg.Column:
  equipment_prices = load_equipement_prices()
  
  layout = [[
    sg.TabGroup([[
      build_tab("Ammo", equipment_prices["ammo"]),
      build_tab("Misc", equipment_prices["misc"]),
      build_tab("Sight", equipment_prices["sight"]),
      build_tab("Optic", equipment_prices["optic"]),
      build_tab("ATV", equipment_prices["atv"]),
      build_tab("Skin", equipment_prices["skin"]),
      build_tab("Weapon", equipment_prices["weapon"]),
      build_tab("Structure", equipment_prices["structure"]),
      build_tab("Lure", equipment_prices["lure"]),
    ]], k="store_group")
  ]]
  return sg.Column(layout)

def handle_event(event: str, window: sg.Window, values: dict) -> None:
  if event.endswith("item_name"):
    type_key = event.split("_")[0]
    item_name = values[event]
    item_index = window[event].Values.index(item_name)
    item_price = window[event].metadata[item_index].price
    window[f"{type_key}_item_price"].update(item_price)

def add_mod(window: sg.Window, values: dict) -> dict:
  active_tab = window["store_group"].get().lower() 
  active_tab = active_tab.split("_")[0]
  
  discount = int(values[f"{active_tab}_discount"])
  free_price = values[f"{active_tab}_free_price"]
  if free_price.isdigit():
    free_price = int(free_price)
  elif free_price != "":
    return {
      "invalid": "Provide a valid free price"
    }    
  else:
    free_price = 0
  discount_or_free_price = discount != 0 or free_price != 0
  
  item_key = f"{active_tab}_item_name"
  item_metadata = window[item_key].metadata
  if not discount_or_free_price:    
    item_name = values[item_key]
    if not item_name:
      return {
        "invalid": "Please select an item first"
      }
    item_index = window[item_key].Values.index(item_name)
    item = item_metadata[item_index]
    item_price = values[f"{active_tab}_item_price"]
    if item_price.isdigit():
      item_price = int(item_price)
    else:
      return {
        "invalid": "Provide a valid item price"
      }
    
    return {
      "key": f"modify_store_{item.name}",
      "invalid": None,
      "options": {
        "type": active_tab,
        "name": item.name,
        "file": EQUIPMENT_FILE,
        "price_offset": item.price_offset,
        "price": item_price,
        "discount": None,
        "free_price": None
      }    
    }
  else:
    return {
      "key": f"modify_store_{active_tab}",
      "invalid": None,
      "options": {
        "type": active_tab,
        "name": None,
        "file": EQUIPMENT_FILE,
        "price_offset": None,
        "price": None,
        "discount": discount,
        "free_price": free_price
    }
  }

def format(options: dict) -> str:
  if options["discount"] or options["free_price"]:
    return f"Modify Store {options['type'].capitalize()} ({options['discount']}%, {options['free_price']})"
  else:
    return f"{options['name']} ({options['price']})"

def handle_key(mod_key: str) -> bool:
  return mod_key.startswith("modify_store")

def get_files(options: dict) -> List[str]:
  return [EQUIPMENT_FILE]

def process(options: dict) -> None:
  file = options["file"]
  if options["discount"] or options["free_price"]:
    discount = options["discount"]
    free_price = options["free_price"]
    prices = load_equipement_prices()[options["type"]]
    if discount != 0:
      offsets = [x.price_offset for x in prices]
      mods.update_file_at_offsets(file, offsets, 1 - discount / 100, transform="multiply")
    if free_price != 0:
      offsets = [x.price_offset for x in prices if x.price == 0]
      mods.update_file_at_offsets(file, offsets, free_price)
  else:
    mods.update_file_at_offset(file, options["price_offset"], options["price"])
