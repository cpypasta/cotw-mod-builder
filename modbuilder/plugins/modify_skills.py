import PySimpleGUI as sg
import textwrap
import modbuilder.plugins.enhanced_soft_feet as enhanced_soft_feet
import modbuilder.plugins.enhanced_pack_mule as enhanced_pack_mule
import modbuilder.plugins.enhanced_impact_resistance as enhanced_impact_resistance
import modbuilder.plugins.enhanced_haggle as enhanced_haggle
import modbuilder.plugins.enhanced_keen_eye as enhanced_keen_eye
import modbuilder.plugins.enhanced_endurance as enhanced_endurance
import modbuilder.plugins.enhanced_improvised_blind as enhanced_improvised_blind
from modbuilder.widgets import create_option, valid_option_value
from modbuilder.mods import update_file_at_offset
from pathlib import Path
from math import floor

DEBUG=False
NAME="Modify Skills"
DESCRIPTION="Modify all skills and perks that have changable values."
FILE = "settings/hp_settings/player_skills.bin"
KEY_PREFIX = "modify_skills"
TABGROUP_PADDING = ((0,0),(10,0))


def name_to_key(skill: str) -> str:
    return "_".join(skill.lower().split(" "))


def key_to_name(skill: str) -> str:
    return " ".join(skill.split("_")).title()


def option_to_key(skill: str, option_name: str) -> str:
    return f"{KEY_PREFIX}_{name_to_key(skill)}__{name_to_key(option_name)}"


def get_active_tab(window: sg.Window) -> str:
    active_tab = window["modify_skills_group"].find_currently_active_tab_key().lower()
    if active_tab == "skills":
        active_tab = window["skill_group"].find_currently_active_tab_key().lower()
        if active_tab == "ambusher":
            active_tab = window["ambusher_group"].find_currently_active_tab_key().lower()
        else:
            active_tab = window["stalker_group"].find_currently_active_tab_key().lower()
    else:
        active_tab = window["perk_group"].find_currently_active_tab_key().lower()
        if active_tab == "rifles":
            active_tab = window["rifle_group"].find_currently_active_tab_key().lower()
        elif active_tab == "handguns":
            active_tab = window["handgun_group"].find_currently_active_tab_key().lower()
        elif active_tab == "shotguns":
            active_tab = window["shotgun_group"].find_currently_active_tab_key().lower()
        else:
            active_tab = window["archery_group"].find_currently_active_tab_key().lower()
    return active_tab    


def get_skill_options(skill: str) -> list[dict]:
    try:
        return globals()[f"render_{skill}"]()
    except:
        return []


def get_skill_option_keys(skill: str) -> list[str]:
    options = get_skill_options(skill)
    skill_options = []
    for option in options:
        skill_options.append(option_to_key(skill, option["name"]))
    return skill_options    


def render_pack_mule() -> list[dict]:
    return enhanced_pack_mule.OPTIONS
def format_pack_mule(options: dict) -> str:
    return enhanced_pack_mule.format(options)
def process_pack_mule(options: dict) -> list[dict]:
    return enhanced_pack_mule.update_values_at_offset(options)   

def render_soft_feet() -> list[dict]:
    return enhanced_soft_feet.OPTIONS
def format_soft_feet(options: dict) -> str:
    return enhanced_soft_feet.format(options)
def process_soft_feet(options: dict) -> list[dict]:
    return enhanced_soft_feet.update_values_at_offset(options)

def render_impact_resistance() -> list[dict]:
    return enhanced_impact_resistance.OPTIONS
def format_impact_resistance(options: dict) -> str:
    return enhanced_impact_resistance.format(options)
def process_impact_resistance(options: dict) -> list[dict]:
    return enhanced_impact_resistance.update_values_at_offset(options)

def render_haggle() -> list[dict]:
    return enhanced_haggle.OPTIONS
def format_haggle(options: dict) -> str:
    return enhanced_haggle.format(options)
def process_haggle(options: dict) -> list[dict]:
    return enhanced_haggle.update_values_at_offset(options)

def render_keen_eye() -> list[dict]:
    return enhanced_keen_eye.OPTIONS
def format_keen_eye(options: dict) -> str:
    return enhanced_keen_eye.format(options)
def process_keen_eye(options: dict) -> list[dict]:
    return enhanced_keen_eye.update_values_at_offset(options)

def render_endurance() -> list[dict]:
    return enhanced_endurance.OPTIONS
def format_endurance(options: dict) -> str:
    return enhanced_endurance.format(options)
def process_endurance(options: dict) -> list[dict]:
    return enhanced_endurance.update_values_at_offset(options)

def render_improvised_blind() -> list[dict]:
    return enhanced_improvised_blind.OPTIONS
def format_improvised_blind(options: dict) -> str:
    return enhanced_improvised_blind.format(options)
def process_improvised_blind(options: dict) -> list[dict]:
    return enhanced_improvised_blind.update_values_at_offset(options)

def render_spotting_knowledge() -> list[dict]:
    return [
        { "name": "Health", "min": 0.00, "max": 1.0, "default": 0.25, "initial": 0.0, "increment": 0.01 },
        { "name": "Score", "min": 0.00, "max": 1.0, "default": 0.1, "initial": 0.0, "increment": 0.01 },
        { "name": "Weight", "min": 0.00, "max": 1.0, "default": 0.25, "initial": 0.0, "increment": 0.01 },
    ]
def format_spotting_knowledge(options: dict) -> str:
    health = options["health"]
    score = options["score"]
    weight = options["weight"]
    return f"Enhanced Spotting Knowledge ({health:.2f} health, {score:.2f} score, {weight:.2f} weight)"
def process_spotting_knowledge(options: dict) -> list[dict]:
    health = options["health"]
    score = options["score"]
    weight = options["weight"]    
    return [
        {
            "offset": 19192,
            "value": f"spotting_show_health(true, {health:>4.2f}), spotting_show_advanced_awareness(true)"
        },
        {
            "offset": 19272,
            "value": f"spotting_show_health(true, {health:>4.2f}), spotting_show_score(true,{score:>4.2f}), spotting_show_weight(true, {weight:>4.2f}), spotting_show_advanced_awareness(true)"
        }
    ]

def render_track_knowledge() -> list[dict]:
    return [
        { "name": "Health", "min": 0.01, "max": 1.0, "default": 0.25, "initial": 0.01, "increment": 0.01},
        { "name": "Weight", "min": 0.00, "max": 1.0, "default": 0.25, "initial": 0.0, "increment": 0.01},
    ]
def format_track_knowledge(options: dict) -> str:
    health = options["health"]
    weight = options["weight"]
    return f"Enhanced Track Knowledge ({health:.2f} health, {weight:.2f} weight)"
def process_track_knowledge(options: dict) -> list[dict]:
    health = options["health"]
    weight = options["weight"]    
    return [
        {
            "offset": 17576,
            "value": f"clue_show_gender(true), clue_show_health(true, {health:>4.2}), clue_show_group_size(true)"
        },
        {
            "offset": 17664,
            "value": f"clue_show_gender(true), clue_show_health(true, {health:>4.2}), clue_show_color(true), clue_show_group_size(true), clue_show_weight(true, {weight:>4.2})"
        }
    ]

def render_locate_tracks() -> list[dict]:
    return [
        { "name": "Angle", "min": 0.0, "max": 45.0, "default": 45.0, "initial": 0.0, "increment": 0.5},
        { "name": "Spawn Distance", "min": 40.0, "max": 99.9, "default": 40.0, "initial": 99.9, "increment": 0.1},
        { "name": "Despawn Distance", "min": 45.0, "max": 99.9, "default": 45.0, "initial": 99.9, "increment": 0.1},
    ]
def format_locate_tracks(options: dict) -> str:
    angle = options["angle"]
    spawn_distance = options["spawn_distance"]
    despawn_distance = options["despawn_distance"]
    return f"Enhanced Locate Tracks ({angle:.2f} angle, {spawn_distance:.2f}m spawn, {despawn_distance:.2f}m despawn)"
def process_locate_tracks(options: dict) -> list[dict]:
    angle = options["angle"]
    spawn_distance = options["spawn_distance"]
    despawn_distance = options["despawn_distance"]    
    angle_whole = floor(angle)
    if angle_whole == 0:
        angle_whole = 1
    return [
        {
            "offset": 16992,
            "value": f"clue_directional_cone_size(MEDIUM, {angle:>4.1f})"
        },
        {
            "offset": 17040,
            "value": f"clue_directional_cone_size(MEDIUM, {angle:>4.1f}), clue_spawn_distance({spawn_distance:>4.1f}, {despawn_distance:>4.1f})"
        },
        {
            "offset": 17120,
            "value": f"clue_directional_cone_size(NARROW, {angle_whole:>2}), clue_spawn_distance({spawn_distance:>4.1f}, {despawn_distance:>4.1f})"
        }
    ]

def render_whos_deer() -> list[dict]:
    return [
        { "name": "Attraction Probability", "min": 2.0, "max": 9.9, "default": 2.0, "initial": 9.9, "increment": 0.1},
        { "name": "Response Probability", "min": 2.0, "max": 5.0, "default": 2.0, "initial": 2.0, "increment": 0.1},
    ]
def format_whos_deer(options: dict) -> str:
    attraction_probability = options["attraction_probability"]
    response_probability = options["response_probability"]
    return f"Enhanced Who's Deer ({attraction_probability:.2f} attraction, {response_probability:.2f} response)"
def process_whos_deer(options: dict) -> list[dict]:
    attraction_probability = options["attraction_probability"]
    response_probability = options["response_probability"]    
    return [
        {
            "offset": 20064,
            "value": f"caller_attraction_probability({attraction_probability:<3.1f})"
        },
        {
            "offset": 20104,
            "value": f"caller_attraction_probability({attraction_probability:<3.1f}), caller_response_probability(ALL, {response_probability:<3.1f})"
        }
    ]

def render_hill_caller() -> list[dict]:
    return [
        { "name": "Attraction Range", "min": 100.0, "max": 999.0, "default": 100.0, "initial": 999.0, "increment": 1.0},
    ]
def format_hill_caller(options: dict) -> str:
    attraction_range = options["attraction_range"]
    return f"Enhanced Hill Caller ({int(attraction_range)}m range)"
def process_hill_caller(options: dict) -> list[dict]:
    attraction_range = options["attraction_range"]
    return [
        {
            "offset": 21248,
            "value": f"increase_caller_item_range_at_lookout_tower({attraction_range:>4.1f})"
        }
    ]

def render_hardened() -> list[dict]:
    return [
        { "name": "Health", "min": 1150.0, "max": 9999.0, "default": 1150.0, "initial": 9999.0, "increment": 1.0},
    ]
def format_hardened(options: dict) -> str:
    health = options["health"]
    return f"Enhaned Hardened ({int(health)})"
def process_hardened(options: dict) -> list[dict]:
    return [
        {
            "offset": 21816,
            "value": f"set_player_max_health({options['health']:>6.1f})"
        }
    ]

def render_im_only_happy_when_it_rains() -> list[dict]:
    return [
        { "name": "Visibility", "min": 0.0, "max": 1.0, "default": 0.9, "initial":1.0, "increment": 0.1},
        { "name": "Hearing", "min": 0.0, "max": 1.0, "default": 1.0, "initial": 1.0, "increment": 0.1},
        { "name": "Scent", "min": 0.0, "max": 1.0, "default": 1.0, "initial": 1.0, "increment": 0.1},
    ]
def format_im_only_happy_when_it_rains(options: dict) -> str:
    visibility = options["visibility"]
    hearing = options["hearing"]
    scent = options["scent"]
    return f"Enhanced I'm Only Happy When It Rains ({visibility} vision, {hearing} hearing, {scent} scent)"
def process_im_only_happy_when_it_rains(options: dict) -> list[dict]:
    visibility = options["visibility"]
    hearing = options["hearing"]
    scent = options["scent"]    
    return [
        {
            "offset": 17256,
            "value": f"weather_animal_senses_multiplier(FOG, {visibility:<3.1f}, {hearing:<3.1f}, {scent:<3.1f})"
        },
        {
            "offset": 17312,
            "value": f"weather_animal_senses_multiplier(FOG, {visibility:<3.1f}, {hearing:<3.1f}, {scent:<3.1f}), weather_animal_senses_multiplier(RAIN, {visibility:<3.1f}, {hearing:<3.1f}, {scent:<3.1f})"
        }
    ]

def render_innate_triangulation() -> list[dict]:
    return [
        { "name": "Indicator Accuracy", "min": 80.0, "max": 99.0, "default": 80.0, "initial": 99.0, "increment": 1.0},
    ]
def format_innate_triangulation(options: dict) -> str:
    indicator_accuracy = options["indicator_accuracy"]
    return f"Enhanced Innate Triangulation ({int(indicator_accuracy)}% accuracy)"
def process_innate_triangulation(options: dict) -> list[dict]:
    indicator_accuracy = int(options["indicator_accuracy"])
    return [
        {
            "offset": 18520,
            "value": f"audio_clue_accuracy({indicator_accuracy})"
        }, 
        {
            "offset": 18544,
            "value": f"audio_clue_accuracy({indicator_accuracy})"
        }
    ]

def render_scent_tinkerer() -> list[dict]:
    return [
        { "name": "Uses", "min": 10.0, "max": 99.0, "default": 10.0, "initial": 99.0, "increment": 1.0, "note": "percent"},
        { "name": "Duration", "min": 300.0, "max": 999.0, "default": 300.0, "initial": 999.0, "increment": 1.0, "note": "seconds"},
        { "name": "Range", "min": 50.0, "max": 99.0, "default": 50.0, "initial": 99.0, "increment": 1.0, "note": "meters"},
        { "name": "Attraction", "min": 50.0, "max": 99.0, "default": 50.0, "initial": 99.0, "increment": 1.0, "note": "percent"},
    ]
def format_scent_tinkerer(options: dict) -> str:
    uses = options["uses"]
    duration = options["duration"]
    range = options["range"]
    attraction = options["attraction"]
    return f"Enhanced Scent Tinkerer ({int(uses)}% uses, {int(duration)}s duration, {int(range)}m range, {int(attraction)}% attraction)"
def process_scent_tinkerer(options: dict) -> list[dict]:
    uses = options["uses"]
    duration = options["duration"]
    range = options["range"]
    attraction = options["attraction"]    
    return [
        {
            "offset": 19480,
            "value": f"increase_scent_item_uses({uses:>4.1f})"
        },
        {
            "offset": 19512,
            "value": f"increase_scent_item_uses({uses:>4.1f}), increase_scent_item_duration({duration:>5.1f})"
        },
        {
            "offset": 19584,
            "value": f"increase_scent_item_uses({uses:>4.1f}), increase_scent_item_duration({duration:>5.1f}), increase_scent_item_range({range:>4.1f})"
        },
        {
            "offset": 19688,
            "value": f"increase_scent_item_uses({uses:>4.1f}), increase_scent_item_duration({duration:>5.1f}), increase_scent_item_range({range:>4.1f}), increase_scent_item_attraction_chance({attraction:>4.1f})"
        },
    ]

def render_tag() -> list[dict]:
    return [
        { "name": "Duration", "min": 2.0, "max": 999.0, "default": 2.0, "initial": 999.0, "increment": 1.0, "note": "seconds"},
        { "name": "Spottable", "min": 3.0, "max": 99.0, "default": 3.0, "initial": 99.0, "increment": 1.0},
    ]
def format_tag(options: dict) -> str:
    duration = int(options["duration"])
    spottable = int(options["spottable"])
    return f"Enhanced Tag ({int(duration)}s duration, {int(spottable)} spottable)"
def process_tag(options: dict) -> list[dict]:
    duration = int(options["duration"])
    spottable = int(options["spottable"])    
    return [
        {
            "offset": 20312,
            "value": f"tag({duration:<3},{spottable:<2})"
        },
        {
            "offset": 20328,
            "value": f"tag({duration:<3},{spottable:<2})"
        }
    ]

def render_the_more_the_merrier() -> list[dict]:
    return [
        { "name": "Reward Multiplier", "min": 5.0, "max": 99.0, "default": 5.0, "initial": 99.0, "increment": 1.0},
    ]
def format_the_more_the_merrier(options: dict) -> str:
    reward_multiplier = int(options["reward_multiplier"])
    return f"Enhanced The More the Merrier ({int(reward_multiplier)}x)"
def process_the_more_the_merrier(options: dict) -> list[dict]:
    reward_multiplier = int(options["reward_multiplier"])    
    return [
        {
            "offset": 20520,
            "value": f"mission_reward_modifier(reward_mission_cash_small,{reward_multiplier:<2}),\nmission_reward_modifier(reward_mission_cash_medium,{reward_multiplier:<2}),\nmission_reward_modifier(reward_mission_cash_large,{reward_multiplier:<2})"
        }
    ]


def render_ranger() -> list[dict]:
    return [
        { "name": "Accuracy", "min": 0.0, "max": 0.05, "default": 0.05, "initial": 0.0, "increment": 0.01},
    ]
def format_ranger(options: dict) -> str:
    accuracy = options["accuracy"]
    return f"Enhanced Ranger ({accuracy:.2f} accuracy)"
def process_ranger(options: dict) -> list[dict]:
    return [
        {
            "offset": 25936,
            "value": f"range_finder({options['accuracy']:<4.2f})"
        }
    ]

def render_fast_shouldering() -> list[dict]:
    return [
        { "name": "Speed Multiplier", "min": 0.0, "max": 10.0, "default": 1.25, "initial": 10.0, "increment": 0.25},
    ]
def format_fast_shouldering(options: dict) -> str:
    speed_multiplier = options["speed_multiplier"]
    return f"Enhanced Fast Shouldering ({speed_multiplier}x)"
def process_fast_shouldering(options: dict) -> list[dict]:
    speed_multiplier = options["speed_multiplier"]
    return [
        {
            "offset": 24960,
            "value": f"in_out_aim_speed(weapon_category_handguns,{speed_multiplier:<4.1f}\n,weapon_category_rifles,{speed_multiplier:<4.1f}\n,weapon_category_bows,{speed_multiplier:<4.1f}\n,weapon_category_shotguns,{speed_multiplier:<4.1f})"
        },
        {
            "offset": 25096,
            "value": f"in_out_aim_speed(weapon_category_handguns,{speed_multiplier:<5.2f}\n,weapon_category_rifles,{speed_multiplier:<5.2f}\n,weapon_category_bows,{speed_multiplier:<5.2f}\n,weapon_category_shotguns,{speed_multiplier:<5.2f})"
        }        
    ]

def render_focused_shot() -> list[dict]:
    return [
        { "name": "Ease In", "min": 0.0, "max": 9.9, "default": 1.5, "initial": 9.9, "increment": 0.1},
        { "name": "Ease Out", "min": 0.0, "max": 9.9, "default": 4.5, "initial": 9.9, "increment": 0.1},
        { "name": "FOV Multiplier", "min": 0.0, "max": 1.0, "default": 0.7, "initial": 0.7, "increment": 0.1},
    ]
def format_focused_shot(options: dict) -> str:
    ease_in = options["ease_in"]
    ease_out = options["ease_out"]
    fov_multiplier = options["fov_multiplier"]
    return f"Enhanced Focused Shot ({ease_in} in, {ease_out} out, {fov_multiplier} FOV)"
def process_focused_shot(options: dict) -> list[dict]:
    ease_in = options["ease_in"]
    ease_out = options["ease_out"]
    fov_multiplier = options["fov_multiplier"]    
    return [
        {
            "offset": 22768,
            "value": f"hold_breath_zoom({ease_in:<3.1f}, {ease_out:<3.1f}, {fov_multiplier:<3.1f})"
        }
    ]

def render_breath_control() -> list[dict]:
    return [
        { "name": "Heart Rate Multiplier", "min": 0.0, "max": 0.096, "default": 0.096, "initial": 0.0, "increment": 0.001},
        { "name": "Hold Breath Multiplier", "min": 0.0, "max": 0.5, "default": 0.5, "initial": 0.0, "increment": 0.1},
        { "name": "Wobble Multiplier", "min": 0.0, "max": 0.66, "default": 0.66, "initial": 0.0, "increment": 0.01},
    ]
def format_breath_control(options: dict) -> str:
    heart_rate_multiplier = options["heart_rate_multiplier"]
    hold_breath_multiplier = options["hold_breath_multiplier"]
    wobble_multiplier = options["wobble_multiplier"]
    return f"Enhanced Breath Control ({heart_rate_multiplier} heart, {hold_breath_multiplier} breath, {wobble_multiplier} wobble)"
def process_breath_control(options: dict) -> list[dict]:
    heart_rate_multiplier = options["heart_rate_multiplier"]
    hold_breath_multiplier = options["hold_breath_multiplier"]
    wobble_multiplier = options["wobble_multiplier"]    
    return [
        {
            "offset": 22960,
            "value": f"breath_out_heart_rate_gain_multiplier({heart_rate_multiplier:>5.3f})"
        },
        {
            "offset": 23008,
            "value": f"breath_out_heart_rate_gain_multiplier({heart_rate_multiplier:>5.3f}), hold_breath_duration_multiplier({hold_breath_multiplier:>3.1f})"
        },
        {
            "offset": 23096,
            "value": f"breath_out_heart_rate_gain_multiplier({heart_rate_multiplier:>5.3f}), hold_breath_duration_multiplier({hold_breath_multiplier:>3.1f}), hold_breath_wobble_multiplier({wobble_multiplier:>4.2f})"            
        }
    ]

def render_steady_hands() -> list[dict]:
    return [
        { "name": "Wobble Multiplier", "min": 0.0, "max": 0.8, "default": 0.8, "initial": 0.0, "increment": 0.1},
    ]
def format_steady_hands(options: dict) -> str:
    wobble_multiplier = options["wobble_multiplier"]
    return f"Enhanced Steady Hands ({wobble_multiplier} wobble)"
def process_steady_hands(options: dict) -> list[dict]:
    wobble_multiplier = options["wobble_multiplier"]
    return [
        {
            "offset": 22856,
            "value": f"base_wobble({wobble_multiplier:<3.1f})"
        },
        {
            "offset": 22880,
            "value": f"base_wobble({wobble_multiplier:<3.1f})"
        }
    ]

def render_survival_instinct() -> list[dict]:
    return [
        { "name": "Duration", "min": 15.0, "max": 99.0, "default": 15.0, "initial": 99.0, "increment": 1.0, "note": "seconds"},
        { "name": "Damage Reduction", "min": 0.0, "max": 0.5, "default": 0.5, "initial": 0.0, "increment": 0.1, "note": "smaller is better"},
    ]
def format_survival_instinct(options: dict) -> str:
    duration = options["duration"]
    damage_reduction = options["damage_reduction"]
    return f"Enhanced Survival Instinct ({int(duration)}s duration, {damage_reduction} damage)"
def process_survival_instinct(options: dict) -> list[dict]:
    duration = options["duration"]
    damage_reduction = options["damage_reduction"]    
    return [
        {
            "offset": 23944,
            "value": f"hurt_animals_damage_less({duration:<4.1f},{damage_reduction:<3.1f})"
        }
    ]

def render_quick_draw() -> list[dict]:
    return [
        { "name": "Speed Multiplier", "min": 1.5, "max": 99.0, "default": 1.5, "initial": 99.0, "increment": 0.5},
        { "name": "Accuracy Multiplier", "min": 0.0, "max": 1.0, "default": 1.0, "initial": 0.0, "increment": 0.01},
    ]
def format_quick_draw(options: dict) -> str:
    speed_multiplier = options["speed_multiplier"]
    accuracy_multiplier = options["accuracy_multiplier"]
    return f"Enhanced Quick Draw ({speed_multiplier}x speed, {accuracy_multiplier}x accuracy)"
def process_quick_draw(options: dict) -> list[dict]:
    speed_multiplier = options["speed_multiplier"]
    speed = f"{speed_multiplier:>4.1f}"
    accuracy_multiplier = options["accuracy_multiplier"]
    accuracy = f"{accuracy_multiplier:>3.2f}"
    return [
        {
            "offset": 24168,
            "value": f"quickshot_speed_scatter(weapon_category_handguns, {speed},{accuracy}\n,weapon_category_rifles, {speed},{accuracy}\n,weapon_category_bows,{speed},{accuracy}\n,weapon_category_shotguns, {speed},{accuracy})"
        },
        {
            "offset": 24336,
            "value": f"quickshot_speed_scatter(weapon_category_handguns,{speed},{accuracy}\n,weapon_category_rifles,{speed},{accuracy}\n,weapon_category_bows,{speed},{accuracy}\n,weapon_category_shotguns,{speed}, {accuracy})"
        },
        {
            "offset": 24504,
            "value": f"quickshot_speed_scatter(weapon_category_handguns,{speed},{accuracy}\n,weapon_category_rifles,{speed},{accuracy}\n,weapon_category_bows,{speed},{accuracy}\n,weapon_category_shotguns,{speed}, {accuracy})"
        }
    ]

def render_quick_feet() -> list[dict]:
    return [
        { "name": "Steady", "min": 2.5, "max": 9.9, "default": 2.5, "initial": 9.9, "increment": 0.1},
    ]
def format_quick_feet(options: dict) -> str:
    steady = options["steady"]
    return f"Enhanced Quick Feet ({steady} steady)"
def process_quick_feet(options: dict) -> list[dict]:
    steady = options["steady"]
    steady = f"{steady:>3.1f}"
    return [
        {
            "offset": 23632,
            "value": f"stance_transition_ended_unsteady_time(weapon_category_handguns,0.0,{steady})"
        },
        {
            "offset": 23704,
            "value": f"stance_transition_ended_unsteady_time(weapon_category_handguns,0.0,{steady})"
        }
    ]

def render_body_control() -> list[dict]:
    return [
        { "name": "Speed Multiplier", "min": 2.0, "max": 9.9, "default": 2.0, "initial": 9.9, "increment": 0.1},
    ]
def format_body_control(options: dict) -> str:
    speed_multiplier = options["speed_multiplier"]
    return f"Enhanced Body Control ({speed_multiplier}x speed)"
def process_body_control(options: dict) -> list[dict]:
    speed_multiplier = options["speed_multiplier"]
    speed = f"{speed_multiplier:>3.1f}"
    return [
        {
            "offset": 25376,
            "value": f"stable_after_rotation({speed})"
        },
        {
            "offset": 25408,
            "value": f"stable_after_rotation({speed})"
        }
    ]

def render_both_eyes_open() -> list[dict]:
    return [
        { "name": "Blur Start", "min": 0.3, "max": 9.9, "default": 0.3, "initial": 9.9, "increment": 0.1},
        { "name": "Blur Amount", "min": 0.0, "max": 0.001, "default": 0.001, "initial": 0.0, "increment": 0.001},
    ]
def format_both_eyes_open(options: dict) -> str:
    blur_start = options["blur_start"]
    blur_amount = options["blur_amount"]
    return f"Enhanced Both Eyes Open ({blur_start} start, {blur_amount} amount)"
def process_both_eyes_open(options: dict) -> list[dict]:
    blur_start = options["blur_start"]
    start = f"{blur_start:>3.1f}"
    blur_amount = options["blur_amount"]    
    amount = f"{blur_amount:>5.3f}"
    return [
        {
            "offset": 24784,
            "value": f"set_iron_sight_blur({start},{amount})"
        },
        {
            "offset": 24816,
            "value": f"set_iron_sight_blur({start}, {amount})"
        }
    ]

def render_recoil_management() -> list[dict]:
    return [
        { "name": "Recoil", "min": 0.0, "max": 0.4, "default": 0.4, "initial": 0.0, "increment": 0.1},
        { "name": "Speed", "min": 1.6, "max": 9.9, "default": 1.6, "initial": 9.9, "increment": 0.1},
    ]
def format_recoil_management(options: dict) -> str:
    recoil = options["recoil"]
    speed = options["speed"]
    return f"Enhanced Recoil Management ({recoil} recoil, {speed} speed)"
def process_recoil_management(options: dict) -> list[dict]:
    recoil = options["recoil"]
    recoil = f"{recoil:>3.1f}"
    speed = options["speed"]  
    speed = f"{speed:>3.1f}"  
    return [
        {
            "offset": 25552,
            "value": f"less_recoil({recoil}, {speed})"
        },
        {
            "offset": 25576,
            "value": f"less_recoil({recoil}, {speed})"
        },
        {
            "offset": 25600,
            "value": f"less_recoil({recoil}, {speed})"
        }
    ]

def render_tracershot() -> list[dict]:
    return [
        { "name": "Tracer Duration", "min": 8.0, "max": 9.9, "default": 8.0, "initial": 9.9, "increment": 0.1 },
        { "name": "Skill Time", "min": 6.0, "max": 9.9, "default": 6.0, "initial": 9.9, "increment": 0.1 },
    ]
def format_tracershot(options: dict) -> str:
    tracer_duration = options["tracer_duration"]
    skill_time = options["skill_time"]
    return f"Enhanced Tracershot ({tracer_duration}s tracer, {skill_time}s skill)"
def process_tracershot(options: dict) -> list[dict]:
    tracer_duration = options["tracer_duration"]
    skill_time = options["skill_time"]    
    return [
        {
            "offset": 25296,
            "value": f"tracershot({tracer_duration:<3.1f},{skill_time:<3.1f})"
        }
    ]

def render_increased_confidence() -> list[dict]:
    return [
        { "name": "Accuracy", "min": 0.0, "max": 1.0, "default": 1.0, "initial": 0.0, "increment": 0.1},
    ]
def format_increased_confidence(options: dict) -> str:
    accuracy = options["accuracy"]
    return f"Enhanced Increased Confidence ({accuracy} accuracy)"
def process_increased_confidence(options: dict) -> list[dict]:
    accuracy = options["accuracy"]
    accuracy = f"{accuracy:>3.1f}"
    return [
        {
            "offset": 26016,
            "value": f"modify_bow_scatter({accuracy})"
        },
        {
            "offset": 26040,
            "value": f"modify_bow_scatter({accuracy})"
        }
    ]

def render_full_draw() -> list[dict]:
    return [
        { "name": "Wobble Start", "min": 32.0, "max": 99.0, "default": 32.0, "initial": 99.0, "increment": 1.0},
        { "name": "Wobble Multiplier", "min": 0.0, "max": 10.0, "default": 10.0, "initial": 0.0, "increment": 1.0},
        { "name": "Hold Duration", "min": 42.0, "max": 999.0, "default": 42.0, "initial": 999.0, "increment": 1.0, "note": "seconds"},
    ]
def format_full_draw(options: dict) -> str:
    wobble_start = options["wobble_start"]
    wobble_multiplier = options["wobble_multiplier"]
    hold_duration = options["hold_duration"]
    return f"Enhanced Full Draw ({wobble_start} start, {wobble_multiplier}x, {hold_duration}s duration)"
def process_full_draw(options: dict) -> list[dict]:
    wobble_start = options["wobble_start"]
    wobble_multiplier = options["wobble_multiplier"]
    hold_duration = options["hold_duration"]
    start = f"{wobble_start:>4.1f}"
    multiplier = f"{wobble_multiplier:>4.1f}"
    hold = f"{hold_duration:>5.1f}"    
    return [
        {
            "offset": 25760,
            "value": f"set_bow_hold_time({start}, {multiplier},{hold})"
        },
        {
            "offset": 25800,
            "value": f"set_bow_hold_time({start}, {multiplier},{hold})"
        },
        {
            "offset": 25840,
            "value": f"set_bow_hold_time({start}, {multiplier},{hold})"
        }
    ]

def render_move_n_shoot() -> list[dict]:
    return [
        { "name": "Steady Multiplier", "min": 3.0, "max": 9.0, "default": 3.0, "initial": 9.0, "increment": 1.0 },
    ]
def format_move_n_shoot(options: dict) -> str:
    steady_multiplier = int(options["steady_multiplier"])
    return f"Enhanced Move n Shoot ({steady_multiplier}x steady)"
def process_move_n_shoot(options: dict) -> list[dict]:
    steady_multiplier = int(options["steady_multiplier"])
    return [
        {
            "offset": 26200,
            "value": f"shoot_and_move({steady_multiplier})"
        }
    ]

def render_pumping_iron() -> list[dict]:
    return [
        { "name": "Draw Length", "min": 1.0, "max": 9.9, "default": 1.0, "initial": 9.9, "increment": 0.1 },
    ]
def format_pumping_iron(options: dict) -> str:
    draw_length = options["draw_length"]
    return f"Enhanced Pumping Iron ({draw_length} draw length)"
def process_pumping_iron(options: dict) -> list[dict]:
    draw_length = options["draw_length"]
    draw = f"{draw_length:>3.1f}"    
    return [
        {
            "offset": 26584,
            "value": f"ammunition_item_total_muzzle_energy_multiplier(equipment_ammo_jp_bow_arrow_300gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_jp_bow_tracer_arrow_300gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_bow_arrow_420gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_bow_tracer_arrow_420gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_bow_arrow_600gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_bow_tracer_arrow_600gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_longbow_arrow_350gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_longbow_tracer_arrow_350gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_longbow_arrow_540gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_longbow_tracer_arrow_540gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_longbow_arrow_700gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_longbow_tracer_arrow_700gr_01, {draw})"
        },
        {
            "offset": 27744,
            "value": f"ammunition_item_total_muzzle_energy_multiplier(equipment_ammo_jp_bow_arrow_300gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_jp_bow_tracer_arrow_300gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_bow_arrow_420gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_bow_tracer_arrow_420gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_bow_arrow_600gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_bow_tracer_arrow_600gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_longbow_arrow_350gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_longbow_tracer_arrow_350gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_longbow_arrow_540gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_longbow_tracer_arrow_540gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_longbow_arrow_700gr_01, {draw}),\nammunition_item_total_muzzle_energy_multiplier(equipment_ammo_bh_longbow_tracer_arrow_700gr_01, {draw})"
        }
    ]

def render_recycle() -> list[dict]:
    return [
        { "name": "Break Chance", "min": 0.0, "max": 25.0, "default": 25.0, "initial": 0.0, "increment": 1.0 },
    ]
def format_recycle(options: dict) -> str:
    break_chance = int(options["break_chance"])
    return f"Enhanced Recycle ({break_chance}% break chance)"
def process_recycle(options: dict) -> list[dict]:
    break_chance = options["break_chance"]
    chance = f"{break_chance:>4.1f}"
    return [
        {
            "offset": 26280,
            "value": f"enable_arrow_retrieval(true), set_arrow_break_on_impact_probability({chance})"
        },
        {
            "offset": 26360,
            "value": f"enable_arrow_retrieval(true), set_arrow_break_on_impact_probability({chance})"
        }
    ]


SKILLS = {
    "Stalker": [
        "Endurance",
        "Hardened",
        "Im Only Happy When It Rains",
        "Improvised Blind",
        "Innate Triangulation",
        "Locate Tracks",
        "Soft Feet",       
        "Track Knowledge",
    ],
    "Ambusher": [
        "Haggle",
        "Hill Caller",
        "Impact Resistance",
        "Keen Eye",
        "Pack Mule",
        "Scent Tinkerer",
        "Spotting Knowledge",
        "Tag",
        "The More the Merrier",
        "Whos Deer",
    ]
}

PERKS = {
    "Rifles": [
        "Breath Control",
        "Focused Shot",
        "Steady Hands",
    ],
    "Handguns": [
        "Survival Instinct",
        "Quick Draw",
        "Quick Feet",
        "Ranger"
    ],
    "Shotguns": [
        "Body Control",
        "Both Eyes Open",
        "Fast Shouldering",
        "Recoil Management",
        "Tracershot"
    ],
    "Archery": [
        "Increased Confidence",
        "Full Draw",
        "Move n Shoot",
        "Pumping Iron",
        "Recycle"
    ],
}

DESCRIPTIONS = {
    "Endurance": "Increase your endurance so that your heart rate rises slower when moving and falls faster when idle.",
    "Hardened": "Increases your health.",
    "Im Only Happy When It Rains": "Decreases your visibility in foggy and rainy weather.",
    "Improvised Blind": "Further decreases your visibility when inside large bushes and shrubs.",
    "Innate Triangulation": "Decreases the size of the animal vocalization indicator.",
    "Locate Tracks": "The directional tracking cone becomes more accurate and narrower. Increases the distance at which tracks are visible and highlighted.",
    "Soft Feet": "Reduces the noise generated when moving through foilage, such as grass and leaves, and larger vegetation, such as bushed and shrubs.",
    "Track Knowledge": "Reveals information about an animal's weight and health.",
    "Haggle": "Reduces the cost of all items in the outpost store.",
    "Hill Caller": "Increases the attraction range of all callers when used near a lookout point or inside an elevated structure like a tree stand or tripod.",
    "Impact Resistance": "Reduces the damage taken from falling.",
    "Keen Eye": "Reveals need zones and animal groups near the lookout point.",
    "Pack Mule": "Increases the base carry capacity.",
    "Scent Tinkerer": "Increases scent usage, duration, range, and attraction.",
    "Spotting Knowledge": "Shows the health, rating, and weight of the spotted animal.",
    "Tag": "Increases the duration and max number of highlighted animals.",
    "The More the Merrier": "Increases the cash reward from completing any mission.",
    "Whos Deer": "Attracts species not normally attracted to the caller and can cause a vocalization response.",
    "Focused Shot": "Holding your breath increases zoom when using rifles with iron, red dot, and holographic sights.",
    "Breath Control": "Steadies a weapon while in aim mode.",
    "Steady Hands": "Decreased wobble when in aim mode using any weapon.",
    "Survival Instinct": "Damage from animal attacks is reduced for a short duration after landing a shot on an aggressive animal.",
    "Quick Draw": "Increases the speed and accuracy of hipshots using any weapon except bows and crossbows.",
    "Quick Feet": "Recover a steady aim faster after changing stances when using handguns.",
    "Ranger": "Increases accuracy when guaging distance of spotted animals.",
    "Body Control": "Weapon sights align faster after rotating with any weapon.",
    "Both Eyes Open": "Decrease edge blur when using shotguns with iron, red dot, and holographic sights.",
    "Fast Shouldering": "Increase the speed of entering and exiting aim mode using any weapon as well as the speed of switching weapons.",
    "Recoil Management": "Less recoil when firing any weapon and able to fire a follow-up shot sooner.",
    "Tracershot": "Ability to trigger a tracer shot when firing shotguns. Pellets will leave behind smoke trails indicating the spread of the bullet.",
    "Increased Confidence": "Increases accuracy of all bows when shooting from the hip.",
    "Full Draw": "Increases the time an arrow can be drawn in aim mode before fatigue sets in.",
    "Move n Shoot": "Decreased wobble while moving in aim mode using any weapon.",
    "Pumping Iron": "Increased arm strength means more draw length. Increases the kinetic energey of all bows which in turn means more damage, penetration, and speed using the same arrows.",
    "Recycle": "Unlocks the ability to retrieve fired arrows and bolts."
}
NOTES = {
    "Spotting Knowledge": "the smaller the value the more accurate the information",
    "Track Knowledge": "the smaller the value the more accurate the information",
    "Breath Control": "the smaller the value the better",
    "Steady Hands": "the smaller the value the better",
}


def get_skill_tab(skills: list[str]) -> list[sg.Tab]:
    skill_options = [get_skill_options(name_to_key(f)) for f in skills]
    skill_details = []

    for i, options in enumerate(skill_options):
        skill_option_details = []
        if skills[i] in DESCRIPTIONS:
            skill_option_details.append([sg.T(textwrap.fill(DESCRIPTIONS[skills[i]], 130), text_color="orange", p=((10, 10),(10,15)))])
        if skills[i] in NOTES:
            skill_option_details.append([sg.T(f"({NOTES[skills[i]]})", text_color="orange", p=((10, 10),(0,0)))])
        for option in options:
            option_key = option_to_key(skills[i], option["name"])
            new_option = create_option(option, option_key)
            new_option[0].append(sg.T(""))
            skill_option_details.extend(new_option)
        skill_option_details.append([sg.T("")])
        skill_details.append(sg.Tab(
            skills[i], 
            skill_option_details, 
            k=name_to_key(skills[i])
        ))    
    return skill_details

def get_skill_elements() -> sg.TabGroup:
    stalker = SKILLS["Stalker"]
    ambusher = SKILLS["Ambusher"]
    
    stalker_options = sg.TabGroup([get_skill_tab(stalker)], k="stalker_group", p=TABGROUP_PADDING)
    ambusher_options = sg.TabGroup([get_skill_tab(ambusher)], k="ambusher_group", p=TABGROUP_PADDING)
    return sg.TabGroup(
        [[sg.Tab("Stalker", [[stalker_options]]), sg.Tab("Ambusher", [[ambusher_options]])
    ]], k="skill_group", p=TABGROUP_PADDING)

def get_perk_elements() -> sg.TabGroup:
    rifle_options = sg.TabGroup([get_skill_tab(PERKS["Rifles"])], k="rifle_group", p=TABGROUP_PADDING)
    handgun_options = sg.TabGroup([get_skill_tab(PERKS["Handguns"])], k="handgun_group", p=TABGROUP_PADDING)
    shotgun_options = sg.TabGroup([get_skill_tab(PERKS["Shotguns"])], k="shotgun_group", p=TABGROUP_PADDING)
    archery_options = sg.TabGroup([get_skill_tab(PERKS["Archery"])], k="archery_group", p=TABGROUP_PADDING)
    return sg.TabGroup(
        [[sg.Tab("Rifles", [[rifle_options]]), sg.Tab("Handguns", [[handgun_options]]), sg.Tab("Shotguns", [[shotgun_options]]), sg.Tab("Archery", [[archery_options]])
    ]], k="perk_group", p=TABGROUP_PADDING)

def get_option_elements() -> sg.Column:
    layout = [
        [sg.TabGroup([[
            sg.Tab("Skills", [[get_skill_elements()]]),
            sg.Tab("Perks", [[get_perk_elements()]])
        ]], k="modify_skills_group", p=TABGROUP_PADDING)],
    ]
    col = sg.Column(layout, expand_x=True)
    return col


def add_mod(window: sg.Window, values: dict) -> dict:
    active_tab = get_active_tab(window)
    skill_options = get_skill_options(active_tab)
    skill_option_keys = get_skill_option_keys(active_tab)

    mod_options = {}
    invalid_result = None
    for i, option in enumerate(skill_option_keys):
        mod_option = option.split("__")[1]
        mod_value = values[option]
        valid_response = valid_option_value(skill_options[i], mod_value)
        if valid_response is None:
            mod_options[mod_option] = values[option]
        else:
            invalid_result = valid_response
            break
    if invalid_result:
        return {
            "invalid": invalid_result
        }
        
        
    mod_options["name"] = key_to_name(active_tab)
    mod_options["key"] = active_tab
    return {
      "key": f"{KEY_PREFIX}_{active_tab}",
      "invalid": None,
      "options": mod_options    
    }

def handle_event(event: str, window: sg.Window, values: dict) -> None:
    pass


def format(options: dict) -> str:
    funcs = globals()
    func_name = f"format_{options['key']}"
    if func_name in funcs:
        return funcs[func_name](options)
    return f"Modify {options['name']}"


def handle_key(mod_key: str) -> bool:
  return mod_key.startswith(KEY_PREFIX)

def process(options: dict) -> None:
    func_name = f"process_{options['key']}"
    if func_name in globals():
        updates = globals()[func_name](options)
        for update in updates:
            update_file_at_offset(Path(FILE), update["offset"], update["value"], update["transform"] if "transform" in update else None)