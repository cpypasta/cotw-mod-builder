from typing import List
from modbuilder import mods

DEBUG = False
NAME = "Modify ATV"
DESCRIPTION = "Allows you to modify the performance of the ATV (all colors). The top speed is not exact, since the acceleration settings will slightly change the top seed. Higher top speeds will need additional acceleration no matter what you pick."
OPTIONS = [
  { "name": "Top Speed", "style": "list", "default": "60", "initial": ["70", "90", "120", "150", "170"] },
  { "name": "Acceleration", "style": "list", "initial": ["default", "medium", "high"] },
  { "name": "Traction", "style": "list", "initial": ["default", "medium", "high"] }
]
SPEED_70 = {
  "gears": [2.2309999465942383, 1.7999999523162842, 1.5290000438690186, 1.277999997138977, 1.0479999780654907, 0.0, 0.0, 0.0],
  "upshift": [6800.0, 6800.0, 6800.0, 6800.0, 6800.0, 0.0, 0.0, 0.0],
  "downshift": [3840.820068359375, 4044.43994140625, 3976.830078125, 3902.60009765625, 0.0, 0.0, 0.0, 0.0],
  "max_rpm": 6850.0,
  "optimal_rpm": 5000.0,
}
SPEED_90 = {
  "gears": [2.2309999465942383, 1.7999999523162842, 1.5290000438690186, 1.277999997138977, 1.0479999780654907, 0.0, 0.0, 0.0],
  "upshift": [8000.0, 8000.0, 8000.0, 8000.0, 8000.0, 0.0, 0.0, 0.0],
  "downshift": [4000.0, 4000.0, 4000.0, 4000.0, 0.0, 0.0, 0.0, 0.0],
  "max_rpm": 8500.0,
  "optimal_rpm": 4000.0,
}
SPEED_120 = {
  "gears": [2.2309999465942383, 1.7999999523162842, 1.5290000438690186, 1.277999997138977, 1.0479999780654907, 0.0, 0.0, 0.0],
  "upshift": [15000.0, 15000.0, 15000.0, 15000.0, 15000.0, 0.0, 0.0, 0.0],
  "downshift": [7500.0, 7500.0, 7500.0, 7500.0, 0.0, 0.0, 0.0, 0.0],
  "max_rpm": 15500.0,
  "optimal_rpm": 5000.0,
}
SPEED_150 = {
  "gears": [2.2309999465942383, 1.7999999523162842, 1.5290000438690186, 1.277999997138977, 1.0479999780654907, 0.0, 0.0, 0.0],
  "upshift": [20000.0, 20000.0, 20000.0, 20000.0, 20000.0, 0.0, 0.0, 0.0],
  "downshift": [10000.0, 10000.0, 10000.0, 10000.0, 0.0, 0.0, 0.0, 0.0],
  "max_rpm": 25000.0,
  "optimal_rpm": 5000.0,
}
SPEED_170 = {
  "gears": [2.2309999465942383, 1.7999999523162842, 1.5290000438690186, 1.277999997138977, 1.0479999780654907, 1.0, 0.0, 0.0],
  "upshift": [20000.0, 20000.0, 20000.0, 20000.0, 20000.0, 20000.0, 0.0, 0.0],
  "downshift": [10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 0.0, 0.0, 0.0],
  "max_rpm": 25000.0,
  "optimal_rpm": 4500.0,
}

TORQUE_DEFAULT = {
  "min": 1.0,
  "max": 0.8999999761581421,
  "optimal": 17.5
}
TORQUE_MEDIUM = {
  "min": 2.0,
  "max": 4.0,
  "optimal": 17.5
}
TORQUE_HIGH = {
  "min": 4.0,
  "max": 12.0,
  "optimal": 14.0
}

TRACTION_DEFAULT = {
  "front_friction": 1.5,
  "rear_friction": 1.5
}
TRACTION_MEDIUM = {
  "front_friction": 2.0,
  "rear_friction": 2.0
}
TRACTION_HIGH = {
  "front_friction": 2.75,
  "rear_friction": 3.0
}

TRANSMISSION_FILE = "editor/entities/vehicles/01_land/v001_car_atv/modules/default/v001_car_atv_transmission.vmodc"
AERODYNAMICS_FILE = "editor/entities/vehicles/01_land/v001_car_atv/modules/default/v001_car_atv_land_aerodynamics.vmodc"
LANDGLOBAL_FILE = "editor/entities/vehicles/01_land/v001_car_atv/modules/default/v001_car_atv_land_global.vmodc"
LANDENGINE_FILE = "editor/entities/vehicles/01_land/v001_car_atv/modules/default/v001_car_atv_land_engine.vmodc"
RED_MERGE_PATH = "editor/entities/vehicles/01_land/v001_car_atv/v001_car_atv_black_red.ee"
SILVER_MERGE_PATH = "editor/entities/vehicles/01_land/v001_car_atv/v001_car_atv_black_silver.ee"
JADE_MERGE_PATH = "editor/entities/vehicles/01_land/v001_car_atv/v001_car_atv_default.ee"

def map_options(options: dict) -> dict:
  top_speed = options["top_speed"] if options["top_speed"] else "70"
  acceleration = options["acceleration"] if options["acceleration"] else "default"
  traction = options["traction"] if options["traction"] else "default"
  
  if top_speed != "70" and acceleration == "default":
    acceleration = "medium"
  elif top_speed == "170" and acceleration != "high":
    acceleration = "high"  
  
  return {
    "top_speed": top_speed,
    "acceleration": acceleration,
    "traction": traction
  }
  

def format(options: dict) -> str:
  options = map_options(options)
  top_speed = options["top_speed"]
  acceleration = options["acceleration"]
  traction = options["traction"]
  return f"Modify ATV ({top_speed}km/h, {acceleration}, {traction})"

def get_files(options: dict) -> List[str]:
  return [TRANSMISSION_FILE, LANDENGINE_FILE, AERODYNAMICS_FILE, LANDGLOBAL_FILE]

def _update_gears(values: List[float], start_offset: int) -> None:
  for i, value in enumerate(values):
      mods.update_file_at_offset(TRANSMISSION_FILE, start_offset + (i * 4), float(value))

def process(options: dict) -> None:
  options = map_options(options)
  top_speed = options["top_speed"] 
  acceleration = options["acceleration"]
  traction = options["traction"]
  
  if top_speed == "90":
    speed_options = SPEED_90
  elif top_speed == "120":
    speed_options = SPEED_120
  elif top_speed == "150":
    speed_options = SPEED_150
  elif top_speed == "170":
    speed_options = SPEED_170
  else:
    speed_options = SPEED_70  
  
  if acceleration == "medium":
    torque_option = TORQUE_MEDIUM
  elif acceleration == "high":
    torque_option = TORQUE_HIGH   
  else:
    torque_option = TORQUE_DEFAULT    
    
  if traction == "medium":
    traction_option = TRACTION_MEDIUM
  elif traction == "high":
    traction_option = TRACTION_HIGH
  else:
    traction_option = TRACTION_DEFAULT
  
  gears = speed_options["gears"]
  upshift = speed_options["upshift"]
  downshift = speed_options["downshift"] 
  
  _update_gears([gears[0], gears[1], gears[2], gears[3], gears[4], gears[5], gears[6], gears[7]], 196)
  _update_gears([upshift[0], upshift[1], upshift[2], upshift[3], upshift[4], upshift[5], upshift[6], upshift[7]], 228)
  _update_gears([downshift[0], downshift[1], downshift[2], downshift[3], downshift[4], downshift[5], downshift[6], downshift[7]], 260)
  
  mods.update_file_at_offset(TRANSMISSION_FILE, 192, 1)  
  mods.update_file_at_offset(TRANSMISSION_FILE, 316, 250.0)  
  mods.update_file_at_offset(TRANSMISSION_FILE, 332, 3.0)
  
  mods.update_file_at_offset(LANDGLOBAL_FILE, 236, traction_option["front_friction"])
  mods.update_file_at_offset(LANDGLOBAL_FILE, 240, 0.0)
  mods.update_file_at_offset(LANDGLOBAL_FILE, 268, traction_option["rear_friction"])  
  mods.update_file_at_offset(LANDGLOBAL_FILE, 272, 0.0)  
  mods.update_file_at_offset(LANDGLOBAL_FILE, 228, 0, format="sint08")  
  mods.update_file_at_offset(LANDGLOBAL_FILE, 260, 0, format="sint08")  
  
  mods.update_file_at_offset(LANDENGINE_FILE, 196, 0.05)
  mods.update_file_at_offset(LANDENGINE_FILE, 208, speed_options["max_rpm"])
  mods.update_file_at_offset(LANDENGINE_FILE, 216, speed_options["optimal_rpm"])
  mods.update_file_at_offset(LANDENGINE_FILE, 220, torque_option["max"])
  mods.update_file_at_offset(LANDENGINE_FILE, 224, torque_option["min"])
  mods.update_file_at_offset(LANDENGINE_FILE, 228, torque_option["optimal"])
  
  mods.update_file_at_offset(AERODYNAMICS_FILE, 192, 1.25)  
  mods.update_file_at_offset(AERODYNAMICS_FILE, 196, 0.3)
  mods.update_file_at_offset(AERODYNAMICS_FILE, 200, 0.3)  

def merge_files(files: List[str]) -> None:
  for bundle_file in [RED_MERGE_PATH, SILVER_MERGE_PATH, JADE_MERGE_PATH]:
    bundle_lookup = mods.get_sarc_file_info(mods.APP_DIR_PATH / "org" / bundle_file)
    for file in files:
      mods.merge_into_file(file, str(bundle_file), bundle_lookup)
  