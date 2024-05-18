# Parses abilities from the game source code and writes them to a JSON file.
# An ability has the following fields:
# - id: the ability's id
# - name: the ability's name
# - description: the ability's description

import re
import resource_manager as rm

# dictionaries related to abilities data
abilities_ids_dict = {}     # ABILITY_XXX --> id
abilities_names_dict = {}   # ABILITY_XXX --> "name"
abilities_desc_dict = {}    # ABILITY_XXX --> "description text"

# builds a dictionary with ability ids as keys and ability numbers as values (ABILITY_XXX, 0)
def build_abilities_ids_dict():
    with open(rm.abilities_ids_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define (ABILITY_\w+)\s+(\d+)', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                abilities_ids_dict[value] = key

# builds a dictionary with ability ids as keys and ability names as values (ABILITY_XXX, "name")
def build_abilities_names_dict():
    with open(rm.abilities_names_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'\s+\[(ABILITY_\w+)\]\s+=\s+_\("(.*)"\)', line)#r'\s+\[(ABILITY_\w+)\]\s+=\s+_\("(.*)"\);'
            if match:
                key = match.group(1)
                value = match.group(2)
                abilities_names_dict[key] = value    

# build a dictionary with ability ids as keys and ability descriptions as values (ABILITY_XXX, "description")
def build_abilities_desc_dict():
    with open(rm.abilities_desc_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

        # obtains the ability id and description text
        pattern = r'static\s+const\s+u8\s+(s\w+)\[\]\s+=\s+_\("(.*)"\);'
        matches = re.findall(pattern, file_content)

        tmp_id_desctxt_dict = {}

        for match in matches:
            key = match[0]
            value = match[1]
            tmp_id_desctxt_dict[key] = value
        
        # maps every ability id to its description text
        pattern = r'\s+\[(ABILITY_\w+)\]\s+=\s+(s\w+),'
        matches = re.findall(pattern, file_content)

        for match in matches:
            key = match[0]
            value = match[1]
            abilities_desc_dict[key] = tmp_id_desctxt_dict[value]

# parses abilities to a JSON file
def parse_to_json():
    abilities_dict = {}
    json_abilities_list = []
    abilities_field_order = ['id', 'name', 'description']
    
    build_abilities_ids_dict()
    build_abilities_names_dict()
    build_abilities_desc_dict()

    for key, value in abilities_ids_dict.items():
        abilities_dict['id'] = key
        abilities_dict['name'] = abilities_names_dict[value]
        abilities_dict['description'] = abilities_desc_dict[value]
        json_abilities_list.append(abilities_dict.copy())
    
    return json_abilities_list
    
