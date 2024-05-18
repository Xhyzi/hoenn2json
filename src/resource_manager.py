import configparser
import os

CONFIG_FILE = 'config.ini'  # config file name, stores files and folders paths

# config.ini path
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIG_FILE)
config = configparser.ConfigParser()
config.read(config_path)

# builds path to the associated files
game_folder_path = config['settings']['game_folder_path']
move_ids_path = os.path.join(game_folder_path, config['settings']['move_ids_file'])
move_names_path = os.path.join(game_folder_path, config['settings']['move_names_file'])
move_desc_path = os.path.join(game_folder_path, config['settings']['move_desc_file'])
move_effect_path = os.path.join(game_folder_path, config['settings']['move_effects_file'])
battle_h_path = os.path.join(game_folder_path, config['settings']['battle_h_file'])
pokemon_h_path = os.path.join(game_folder_path, config['settings']['pokemon_h_file'])
type_names_file = os.path.join(game_folder_path, config['settings']['type_names_file'])
move_effects2_path = os.path.join(game_folder_path, config['settings']['move_effects2_file'])
move_flags_path = os.path.join(game_folder_path, config['settings']['move_flags_file'])
move_data_file = os.path.join(game_folder_path, config['settings']['move_data_file'])

# abilities data
abilities_ids_path = os.path.join(game_folder_path, config['settings']['abilities_ids_file'])
abilities_names_path = os.path.join(game_folder_path, config['settings']['abilities_names_file'])
abilities_desc_path = os.path.join(game_folder_path, config['settings']['abilities_desc_file'])

# growth rates data
growth_rates_ids_path = os.path.join(game_folder_path, config['settings']['growth_rate_ids_file'])

# items data
item_ids_path = os.path.join(game_folder_path, config['settings']['item_ids_file'])
item_desc_path = os.path.join(game_folder_path, config['settings']['item_desc_file'])
item_pockets_path = os.path.join(game_folder_path, config['settings']['item_pockets_file'])
item_types_path = os.path.join(game_folder_path, config['settings']['item_types_file'])
hold_effects_path = os.path.join(game_folder_path, config['settings']['hold_effects_file'])
battle_usages_path = os.path.join(game_folder_path, config['settings']['battle_usages_file'])
items_data_file = os.path.join(game_folder_path, config['settings']['items_data_file'])

# pokedex entries data
dex_desc_path = os.path.join(game_folder_path, config['settings']['dex_desc_file'])
dex_data_file = os.path.join(game_folder_path, config['settings']['dex_data_file'])
dex_national_ids_file = os.path.join(game_folder_path, config['settings']['dex_national_ids_file'])

# pokemon data
species_names_path = os.path.join(game_folder_path, config['settings']['species_names_file'])

# output files
output_dir = config['output']['output_dir']
moves_output_file = os.path.join(output_dir, config['output']['moves_output_file'])
abilities_output_file = os.path.join(output_dir, config['output']['abilities_output_file'])
growth_rates_output_file = os.path.join(output_dir, config['output']['growth_rates_output_file'])
items_output_file = os.path.join(output_dir, config['output']['items_output_file'])
dex_entries_output_file = os.path.join(output_dir, config['output']['dex_entries_output_file'])
