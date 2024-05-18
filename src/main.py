# ########################################################## #
# ################### Hoenn to JSON ######################## #
# ########################################################## #
# This script parses data from the Pokémon Hoenn Adventures  #
# game source code and writes it to JSON files located at:   #
#       ./output/<file>.json                                 #
# ########################################################## #
# Pokemon Hoenn Adventures is a fan-made game developed by   #
# Team Hoenn, based on pret's pokeeemerald disassembly       #
# open-source project.                                       #
# This script should be able to work with any game based on  #
# pret's disassembly with minor modifications.               #
# ########################################################## #
# NOTE: modify config.ini so game_folder_path points to the  #
# root folder of your game's source code.                    #
# ########################################################## #

# Importing modules
import json
import resource_manager as rm
import parser_moves as pm
import parser_abilities as pa
import parser_growth_rates as pgr
import parser_items as pi
import parser_dex_entries as pde

# TODO: add cmd line support to pass params (game folder path, if not use config as default)
# TODO: add cmd line support for a "clean" option to remove output files
# TODO: add message of successfull creation of each file

# Generates moves.json
json_moves_list = pm.parse_to_json(rm.move_data_file) 
with open(rm.moves_output_file, 'w', encoding='utf-8') as f:
    json.dump(json_moves_list, f, indent=4, ensure_ascii=False)

# Generates abilities.json
json_abilities_list = pa.parse_to_json()
with open('../output/abilities.json', 'w', encoding='utf-8') as f:
    json.dump(json_abilities_list, f, indent=4, ensure_ascii=False)

# Generates growth_rates.json
json_growth_rates_list = pgr.parse_to_json()
with open('../output/growth_rates.json', 'w', encoding='utf-8') as f:
    json.dump(json_growth_rates_list, f, indent=4, ensure_ascii=False)

# Generates items.json
json_items_list = pi.parse_to_json(rm.items_data_file)
with open('../output/items.json', 'w', encoding='utf-8') as f:
    json.dump(json_items_list, f, indent=4, ensure_ascii=False)    

# Generates dex_entries.json
json_dex_entries_list = pde.parse_to_json(rm.dex_data_file)
with open('../output/dex_entries.json', 'w', encoding='utf-8') as f:
    json.dump(json_dex_entries_list, f, indent=4, ensure_ascii=False)
