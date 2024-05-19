# Parses pokemon species from the game source code and writes them to a JSON file.
# An item has the following fields:
# - species_id:         the species' id
# - name:               the species' name
# - dex_num:            the species' dex_num
# - types[2]:            the species' types
# - base_hp:            the species' base_hp
# - base_atk:           the species' base_atk
# - base_def:           the species' base_def
# - base_spd:           the species' base_spd
# - base_sp_atk:        the species' base_sp_atk
# - base_sp_def:        the species' base_sp_def
# - abilities[2]:       the species' abilities
# - hidden_ability:     the species' hidden ability
# - catch_rate:         the species' catch rate
# - growth_rate:        the species growth rate
# - exp_yield:          the species' exp yield
# - ev_yield[6]:        the species' ev yield
# - female_ratio:       the species female ratio
# - egg_cycles:         the species egg cycles
# - egg_groups[2]:      the species egg groups
# - friendship:         the species friendship
# - body_color:         the species body color
# - items[2]:           the species items
# - safari_flee_rate:   the species safari flee rate -> this is actually unused
# - flags[]:            the species flags
# TODO: moves
    # TODO: level_up_learnsets  (level, move)
    # TODO: evolution_moves     (move)
    # TODO: mt/hm moves         (move)
    # TODO: egg moves           (move)
    # TODO: hoenn tutor moves   (badge, move)
# TODO: evolutions
# TODO: forms

# To be parsed on the future
#

import re
import resource_manager as rm
import parser_moves as pm
import parser_abilities as pa
import parser_items as pit

species_ids_dict = {}           # SPECIES_XXX --> id
species_names_dict = {}         # SPECIES_XXX --> name
species_dex_nums_dict = {}      # SPECIES_XXX --> dex_num
egg_groups_dict = {}            # EGG_GROUP_XXX --> egg group
types_dict = {}                 # TYPE_XXX --> type
abilities_dict = {}             # ABILITY_XXX --> ability

abilities_dict = pa.build_abilities_names_dict()

# builds a dictionary with species ids and their numbers (SPECIES_XXX, 0)
def build_species_ids_dict():
    with open(rm.species_ids_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define (SPECIES_\w+)\s+(\d+)', line)
            if match:
                key = re.sub(r'SPECIES_', '', match.group(1))
                value = match.group(2)
                species_ids_dict[key] = value

# builds a dictionary with species names (SPECIES_XXX, name)
def build_species_names_dict():
    with open(rm.species_names_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'\s+\[SPECIES_(\w+)\]\s+=\s+_\("(.*)"\)', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                species_names_dict[key] = value

# builds a dictionary with species dex numbers (SPECIES_XXX, dex_num)
def build_species_dex_nums_dict():
    with open(rm.dex_national_ids_file, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define\s+(NATIONAL_DEX_\w+)\s+(\d+)', line)
            if match:
                key = re.sub(r'NATIONAL_DEX_', '', match.group(1))
                value = match.group(2)
                species_dex_nums_dict[key] = value

# builds a dictionary with egg groups (EGG_GROUP_XXX, egg group)
def build_egg_groups_dict():
    with open(rm.egg_groups_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define\s+(EGG_GROUP_\w+)\s+(\d+)', line)
            if match:
                key = match.group(1)
                value = re.sub(r'EGG_GROUP_', '', key)
                value = value.lower()
                egg_groups_dict[key] = value

def build_types_dict():
    tmp_types_indexes = pm.build_types_dict() # TYPES_XXX --> id
    tmp_types_names = pm.build_type_names_dict() # id --> name

    for key, value in tmp_types_indexes.items():
        if key == 'TYPE_NONE':
            continue
        types_dict[key] = tmp_types_names[tmp_types_indexes[key]]

def fix_properties_abilities(properties):
    pattern = r'{ABILITY_\w+,\s+ABILITY_\w+'
    matches = re.findall(pattern, properties)

    for match in matches:
        properties = re.sub(match, match + '},', properties)
    return properties
            

def parse_to_json(species_file):

    species_dict = {}
    json_species_list = []

    build_species_ids_dict()
    build_species_names_dict()
    build_species_dex_nums_dict()
    build_egg_groups_dict()
    build_types_dict()

    with open(species_file, 'r', encoding='utf-8') as f:
        file_content = f.read()

        species_fields_order = ['name', 'dex_num', 'types', 'base_hp', 'base_atk', 'base_def', 'base_spd', 'base_sp_atk', 'base_sp_def', 'abilities', 'hidden_ability', 'catch_rate', 'growth_rate', 'exp_yield', 'ev_yield', 'female_ratio', 'egg_cycles', 'egg_groups', 'friendship', 'body_color', 'items', 'safari_flee_rate', 'flags']
        ignored_species = ['MEGA', 'PRIMAL', 'ALOLAN', 'GALARIAN', 'PIKACHU_', 'PICHU_', 'UNOWN_', 'CASTFORM_', 'DEOXYS_', 'BURMY_', 'WORMADAM_', 'CHERRIM_', 'SHELLOS_', 'GASTRODON_', 'ROTOM_', 'GIRATINA_', 'SHAYMIN_', 'ARCEUS_', 'BASCULIN_', 'DARMANITAN_', 'DEERLING_', 'SAWSBUCK_', 'TORNADUS_', 'THUNDURUS_', 'LANDORUS_', 'KYUREM_', 'KELDEO_', 'MELOETTA_', 'GENESECT_', 'VIVILLON_', 'FLABEBE_', 'FLOETTE_', 'FLORGES_', 'FURFROU_', 'AEGISLASH_', 'PUMPKABOO_', 'GOURGEIST_', 'XERNEAS_', 'YVELTAL_', 'ZYGARDE_', 'HOOPA_', 'ORICORIO_', 'LYCANROC_', 'WISHIWASHI_', 'MINIOR_', 'MIMIKYU_', 'NECROZMA_', 'ZERAORA_', 'MELTAN_', 'MELMETAL_', 'ZACIAN_', 'ZAMAZENTA_', 'ETERNATUS_', 'URSHIFU_', 'CALYREX_', 'GRENINJA_', 'MEOWSTIC_', 'ROCKRUFF_', 'SILVALLY_', 'MAGEARNA_', 'CRAMORANT_', 'TOXTRICITY_', 'SINISTEA_', 'POLTEAGEIST_', 'ALCREMIE_', 'EISCUE_', 'INDEEDEE_', 'MORPEKO_', 'ZARUDE_', 'SCARF_', 'SALANDIT_FEM', '_GIGA', '_HOENNIAN']

        # pattern to match every item data block
        pattern = re.compile(r'\[(\w+)\]\s*=\s*\{\s*(.*?)\s*\},\n\n', re.DOTALL)

        # pattern to match each item property
        property_pattern = re.compile(r'\.(\w+)\s*=\s*([^,]+),')
        abilities_pattern = r'{ABILITY_\w+,\s+ABILITY_\w+}'

        for match in pattern.finditer(file_content):
            species_id = re.sub(r'SPECIES_', '', match.group(1))
            species_properties = match.group(2)
            species_properties = fix_properties_abilities(species_properties)            

            if any(sp in species_id for sp in ignored_species):
                continue

            properties = {}
            properties['name'] = species_names_dict[species_id]
            properties['dex_num'] = species_dex_nums_dict[species_id]

            types = []
            egg_groups = []
            evs_yield = []
            items = []

            for prop_match in property_pattern.finditer(species_properties):
                key = prop_match.group(1)
                value = prop_match.group(2)

                if value.isdigit():
                    value = int(value)
                elif value == 'TRUE':
                    value = True
                elif value == 'FALSE':
                    value = False

                if key == 'type1':
                    types.append(types_dict[value])
                    continue
                elif key == 'type2':
                    if types_dict[value] != types[0]:
                        types.append(types_dict[value])
                    key = 'types'
                    value = types
                elif key == 'baseHP':
                    key = 'base_hp'
                elif key == 'baseAttack':
                    key = 'base_atk'
                elif key == 'baseDefense':
                    key = 'base_def'
                elif key == 'baseSpeed':
                    key = 'base_spd'
                elif key == 'baseSpAttack':
                    key = 'base_sp_atk'
                elif key == 'baseSpDefense':
                    key = 'base_sp_def'
                elif key == 'catchRate':
                    key = 'catch_rate'
                elif key == 'expYield':
                    key = 'exp_yield'
                elif 'evYield_' in key and value > 0:
                    stat = re.sub(r'evYield_', '', key).lower()
                    if 'speed' not in stat:
                        stat = re.sub(r'sp', 'sp_', stat)
                    evs_yield.append([stat, value])
                    continue          
                elif key == 'abilities':
                    tmp = re.search(abilities_pattern, species_properties)
                    tmp = re.sub(r'{|}', '', tmp.group(0))
                    tmp = tmp.split(',')
                    tmp = [s.strip() for s in tmp]
                    value = [abilities_dict[tmp[0]], abilities_dict[tmp[1]]]
                elif key == 'abilityHidden':
                    key = 'hidden_ability'
                    value = abilities_dict[value]
                elif key == 'bodyColor':
                    key = 'body_color'
                    value = re.sub(r'BODY_COLOR_', '', value).lower()
                elif key == 'growthRate':
                    key = 'growth_rate'
                    value = re.sub(r'GROWTH_', '', value).lower()
                elif key == 'genderRatio':
                    key = 'female_ratio'
                    if 'PERCENT_FEMALE' in value:
                        value = re.sub(r'PERCENT_FEMALE|\(|\)', '', value)
                        value = float(value) / 100
                    elif 'MON_MALE' in value:
                        value = 0
                    elif 'MON_FEMALE' in value:
                        value = 1.0
                    elif 'MON_GENDERLESS' in value:
                        value = 'genderless'
                elif key == 'eggCycles':
                    key = 'egg_cycles'
                elif key == 'eggGroup1':
                    egg_groups.append(egg_groups_dict[value])
                    continue
                elif key == 'eggGroup2':
                    if egg_groups_dict[value] != egg_groups[0]:
                        egg_groups.append(egg_groups_dict[value])
                    key = 'egg_groups'
                    value = egg_groups
                elif key == 'item1':
                    items.append(pit.item_names_dict[value])
                    continue
                elif key == 'item2':
                    if value not in items:
                        items.append(pit.item_names_dict[value])
                    key = 'items'
                    value = items
                elif key == 'flags':
                    value = re.sub(r'F_', '', value).lower()
                
                    

                # TODO: check if properties key already has a value to avoid repeated ones
                properties[key] = value

            properties['ev_yield'] = evs_yield

            ordered_properties = {key: properties.get(key, "none" if key == 'hold_effect' or key == 'battle_usage' else 0) for key in species_fields_order}

            species_dict[species_id] = ordered_properties

        for key, value in species_dict.items():
            json_species_list.append(value)
        return json_species_list
                    
                # if prop_key == 'species':
                #     prop_value = species_names_dict[prop_value]
                # elif prop_key == 'types':
                #     prop_value = [prop_value, '']
                # elif prop_key == 'abilities':
                #     prop_value = [prop_value, '']
                # elif prop_key == 'hidden_ability':
                #     prop_value = species_names_dict[prop_value]
                # elif prop_key == 'egg_groups':
                #     prop_value = [prop_value, '']
                # elif prop_key == 'growth_rate':
                #     prop_value = prop_value
                # elif prop_key == 'items':
                #     prop_value = [prop_value, '']
                # elif prop_key == 'flags':
                #     prop_value = [prop_value, '']
                # else:
                #     prop_value = prop_value

                #properties[key] = value

    #return -1