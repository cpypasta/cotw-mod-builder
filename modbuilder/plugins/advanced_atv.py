from typing import List
from modbuilder import mods

DEBUG=True
NAME = "Advanced ATV"
DESCRIPTION = "Allows you to modify the ATV."
OPTIONS = [
  { "title": "Gear Ratios" },
  { "name": "gr1", "style": "inline", "min": 0, "max": 10, "initial": 4.0 },
  { "name": "gr2", "style": "inline", "min": 0, "max": 10, "initial": 2.5 },
  { "name": "gr3", "style": "inline", "min": 0, "max": 10, "initial": 1.600000023841858 },
  { "name": "gr4", "style": "inline", "min": 0, "max": 10, "initial": 1.399999976158142 },
  { "name": "gr5", "style": "inline", "min": 0, "max": 10, "initial": 1.1699999570846558 },
  { "name": "gr6", "style": "inline", "min": 0, "max": 10, "initial": 1.149999976158142 },
  { "name": "gr7", "style": "inline", "min": 0, "max": 10, "initial": 1.0499999523162842 },
  { "name": "gr8", "style": "inline", "min": 0, "max": 10, "initial": 0.949999988079071 },
  { "title": "Upshift RPM" },
  { "name": "ur1", "style": "inline", "min": 0, "max": 20000, "initial": 8000.0 },
  { "name": "ur2", "style": "inline", "min": 0, "max": 20000, "initial": 8000.0 },
  { "name": "ur3", "style": "inline", "min": 0, "max": 20000, "initial": 8000.0 },
  { "name": "ur4", "style": "inline", "min": 0, "max": 20000, "initial": 8000.0 },
  { "name": "ur5", "style": "inline", "min": 0, "max": 20000, "initial": 8000.0 },
  { "name": "ur6", "style": "inline", "min": 0, "max": 20000, "initial": 8000.0 },
  { "name": "ur7", "style": "inline", "min": 0, "max": 20000, "initial": 8000.0 },
  { "name": "ur8", "style": "inline", "min": 0, "max": 20000, "initial": 8000.0 },
  { "title": "Downshift RPM" },
  { "name": "dr1", "style": "inline", "min": 0, "max": 20000, "initial": 7000.0 },    
  { "name": "dr2", "style": "inline", "min": 0, "max": 20000, "initial": 7000.0 },    
  { "name": "dr3", "style": "inline", "min": 0, "max": 20000, "initial": 7000.0 },    
  { "name": "dr4", "style": "inline", "min": 0, "max": 20000, "initial": 7000.0 },    
  { "name": "dr5", "style": "inline", "min": 0, "max": 20000, "initial": 7000.0 },    
  { "name": "dr6", "style": "inline", "min": 0, "max": 20000, "initial": 7000.0 },    
  { "name": "dr7", "style": "inline", "min": 0, "max": 20000, "initial": 7000.0 },    
  { "name": "dr8", "style": "inline", "min": 0, "max": 20000, "initial": 0.0 },
  { "title": "Gear Misc" },
  { "name": "Nitrous Gears", "style": "inline", "initial": True },
  { "name": "Max RPM", "style": "inline", "min": 0, "max": 200000, "initial": 15000.0 },
  { "name": "Optimal RPM", "style": "inline", "min": 0, "max": 20000, "initial": 3500.0 },
  { "name": "Reverse Gear Ratio", "style": "inline", "min": 0, "max": 10, "initial": 3.0 },
  { "name": "Resistance at Max RPM", "style": "inline", "min": 0, "max": 10, "initial": 0.05 },
  { "name": "Torque Factor at Min RPM", "style": "inline", "min": 0, "max": 20, "initial": 4.0 },
  { "name": "Torque Factor at Max RPM", "style": "inline", "min": 0, "max": 20, "initial": 12.0 },
  { "name": "Torque Factor at Optimal RPM", "style": "inline", "min": 0, "max": 30, "initial": 14.0 },
  { "title": "Aerodynamics and Drag" },
  { "name": "Max Speed", "style": "inline", "min": 60, "max": 300, "initial": 250.0 },
  { "name": "Drag Coefficient", "style": "inline", "min": 0, "max": 10, "initial": 0.3 },
  { "name": "Top Speed Drag Coefficient", "style": "inline", "min": 0, "max": 10, "initial": 0.3 },
  { "name": "Front Area", "style": "inline", "min": 0, "max": 10, "initial": 1.25 },
  { "name": "Front Wheels Arcade Friction Multiplier", "style": "inline", "min": 0, "max": 10, "initial": 2.75 },
  { "name": "Rear Wheels Arcade Friction Multiplier", "style": "inline", "min": 0, "max": 10, "initial": 3.5 },  
  { "name": "Front Wheels Arcade Drag Multiplier", "style": "inline", "min": 0, "max": 1, "initial": 0.0 },
  { "name": "Rear Wheels Arcade Drag Multiplier", "style": "inline", "min": 0, "max": 1, "initial":  0.0 },
  { "name": "Front Wheels Use Shape Cast", "style": "inline", "initial":  False },
  { "name": "Rear Wheels Use Shape Cast", "style": "inline", "initial":  False }
  
]
TRANSMISSION_FILE = "editor/entities/vehicles/01_land/v001_car_atv/modules/default/v001_car_atv_transmission.vmodc"
AERODYNAMICS_FILE = "editor/entities/vehicles/01_land/v001_car_atv/modules/default/v001_car_atv_land_aerodynamics.vmodc"
LANDGLOBAL_FILE = "editor/entities/vehicles/01_land/v001_car_atv/modules/default/v001_car_atv_land_global.vmodc"
LANDENGINE_FILE = "editor/entities/vehicles/01_land/v001_car_atv/modules/default/v001_car_atv_land_engine.vmodc"
RED_MERGE_PATH = "editor/entities/vehicles/01_land/v001_car_atv/v001_car_atv_black_red.ee"
SILVER_MERGE_PATH = "editor/entities/vehicles/01_land/v001_car_atv/v001_car_atv_black_silver.ee"
JADE_MERGE_PATH = "editor/entities/vehicles/01_land/v001_car_atv/v001_car_atv_default.ee"

def format(options: dict) -> str:
  return f"Advanced ATV"

def get_files(options: dict) -> List[str]:  
  return [TRANSMISSION_FILE, LANDENGINE_FILE, AERODYNAMICS_FILE, LANDGLOBAL_FILE]

def _update_gears(values: List[float], start_offset: int) -> None:
  for i, value in enumerate(values):
      mods.update_file_at_offset(TRANSMISSION_FILE, start_offset + (i * 4), float(value))

def process(options: dict) -> None:
  gr1 = float(options["gr1"])
  gr2 = float(options["gr2"])
  gr3 = float(options["gr3"])
  gr4 = float(options["gr4"])
  gr5 = float(options["gr5"])
  gr6 = float(options["gr6"])
  gr7 = float(options["gr7"])
  gr8 = float(options["gr8"])
  
  ur1 = float(options["ur1"])
  ur2 = float(options["ur2"])
  ur3 = float(options["ur3"])
  ur4 = float(options["ur4"])
  ur5 = float(options["ur5"])
  ur6 = float(options["ur6"])
  ur7 = float(options["ur7"])
  ur8 = float(options["ur8"])
  
  dr1 = float(options["dr1"])
  dr2 = float(options["dr2"])
  dr3 = float(options["dr3"])
  dr4 = float(options["dr4"])
  dr5 = float(options["dr5"])
  dr6 = float(options["dr6"])
  dr7 = float(options["dr7"])
  dr8 = float(options["dr8"]  )
  
  _update_gears([gr1, gr2, gr3, gr4, gr5, gr6, gr7, gr8], 196)
  _update_gears([ur1, ur2, ur3, ur4, ur5, ur6, ur7, ur8], 228)
  _update_gears([dr1, dr2, dr3, dr4, dr5, dr6, dr7, dr8], 260)
  
  nitrous_gears = 1 if options["nitrous_gears"] else 0
  max_rpm = float(options["max_rpm"])
  optimal_rpm = float(options["optimal_rpm"])
  reverse_gear_ratio = float(options["reverse_gear_ratio"])
  resistance_max_rpm = float(options["resistance_at_max_rpm"])
  torque_at_min_rpm = float(options["torque_factor_at_min_rpm"])
  torque_at_max_rpm = float(options["torque_factor_at_max_rpm"])
  torque_at_optimal_rpm = float(options["torque_factor_at_optimal_rpm"])
  drag_co = float(options["drag_coefficient"])
  top_speed_drag_co = float(options["top_speed_drag_coefficient"])
  front_wheels_friction = float(options["front_wheels_arcade_friction_multiplier"])
  rear_wheels_friction = float(options["rear_wheels_arcade_friction_multiplier"])
  front_wheels_drag = float(options["front_wheels_arcade_drag_multiplier"])
  rear_wheels_drag = float(options["rear_wheels_arcade_drag_multiplier"])
  max_speed = float(options["max_speed"])
  front_area = float(options["front_area"])
  front_wheel_shape_cast = 1 if options["front_wheels_use_shape_cast"] else 0
  rear_wheel_shape_cast = 1 if options["rear_wheels_use_shape_cast"] else 0
  
  mods.update_file_at_offset(TRANSMISSION_FILE, 192, nitrous_gears)  
  mods.update_file_at_offset(TRANSMISSION_FILE, 316, max_speed)  
  mods.update_file_at_offset(TRANSMISSION_FILE, 332, reverse_gear_ratio)
  
  mods.update_file_at_offset(LANDGLOBAL_FILE, 236, front_wheels_friction)
  mods.update_file_at_offset(LANDGLOBAL_FILE, 240, front_wheels_drag)
  mods.update_file_at_offset(LANDGLOBAL_FILE, 268, rear_wheels_friction)  
  mods.update_file_at_offset(LANDGLOBAL_FILE, 272, rear_wheels_drag)  
  mods.update_file_at_offset(LANDGLOBAL_FILE, 228, front_wheel_shape_cast, format="sint08")  
  mods.update_file_at_offset(LANDGLOBAL_FILE, 260, rear_wheel_shape_cast, format="sint08")  
  
  mods.update_file_at_offset(LANDENGINE_FILE, 196, resistance_max_rpm)
  mods.update_file_at_offset(LANDENGINE_FILE, 208, max_rpm)
  mods.update_file_at_offset(LANDENGINE_FILE, 216, optimal_rpm)
  mods.update_file_at_offset(LANDENGINE_FILE, 220, torque_at_max_rpm)
  mods.update_file_at_offset(LANDENGINE_FILE, 224, torque_at_min_rpm)
  mods.update_file_at_offset(LANDENGINE_FILE, 228, torque_at_optimal_rpm)
  
  mods.update_file_at_offset(AERODYNAMICS_FILE, 192, front_area)  
  mods.update_file_at_offset(AERODYNAMICS_FILE, 196, drag_co)
  mods.update_file_at_offset(AERODYNAMICS_FILE, 200, top_speed_drag_co)

def merge_files(files: List[str]) -> None:
  for bundle_file in [RED_MERGE_PATH, SILVER_MERGE_PATH, JADE_MERGE_PATH]:
    bundle_lookup = mods.get_sarc_file_info(mods.APP_DIR_PATH / "org" / bundle_file)
    for file in files:
      mods.merge_into_file(file, str(bundle_file), bundle_lookup)
  