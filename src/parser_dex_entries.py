# Parses dex entries from the game source code and writes them to a JSON file.
# A dex entry has the following fields:
# - species:        the dex entry's species name
# - national_id:    the dex entry's national id
# - region_id:      the dex entry's id
# - category:       the dex entry's category
# - height:         the dex entry's height
# - weight:         the dex entry's weight
# - description:    the dex entry's description

import resource_manager as rm
import re

species_names_dict = {}     # BULBASAUR: "bulbasaur"
national_ids_dict = {}      # NATIONAL_DEX_BULBASAUR: 1
regional_ids_dict = {}      # HOENN_DEX_TREECKO: 1
dex_desc_dict = {}          # gBulbasaurPokedexText: "description text"

# builds a dictionary with species ids as keys and species names as values (SPECIES_XXX, "name")
def build_species_names_dict():
    with open(rm.species_names_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'\s+\[SPECIES_(\w+)\]\s+=\s+_\("(.*)"\)', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                species_names_dict[key] = value

# builds a dictionary with national ids as keys and national numbers as values (NATIONAL_DEX_XXX, 0)
def build_national_ids_dict():
    with open(rm.dex_national_ids_file, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define\s+(NATIONAL_DEX_\w+)\s+(\d+)', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                national_ids_dict[key] = value

# builds a dictionary with regional ids as keys and regional numbers as values (HOENN_DEX_XXX, 0)
def build_regional_ids_dict():
    with open(rm.dex_national_ids_file, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define\s+(HOENN_DEX_\w+)\s+(\d+)', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                regional_ids_dict[key] = value

# builds a dictionary with dex descriptions ids as keys and dex descriptions as values (gXXXPokedexText, "description text")
def build_dex_desc_dict():
    with open(rm.dex_desc_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

        pattern = r'const\su8\s(\w+)\[\]\s=\s_\(\s*"((?:.|\n)*?)"\);'
        matches = re.findall(pattern, file_content)

        for match in matches:
            key = match[0]
            desc = re.sub(r'\\n|"|\t', '', match[1])    # replaces \n and " with empty string
            desc = re.sub(r'\n', ' ', desc)             # replaces \n with space
            desc = re.sub(r'\s+', ' ', desc)            # replaces multiple spaces with single space
            desc = re.sub(r'-\s+', '', desc)            # replaces '- ' with empty string
            dex_desc_dict[key] = desc

# parses dex entries to a JSON file
def parse_to_json(dex_entries_file):

    dex_entries_dict = {}
    json_dex_entries_list = []

    dex_fields_order = ['species', 'national_id', 'regional_id', 'category', 'height', 'weight', 'description']
    ignored_fields = ['pokemonScale', 'pokemonOffset', 'trainerScale', 'trainerOffset'] # this fields will not make it to the JSON file

    # builds dictionaries
    build_species_names_dict()
    build_national_ids_dict()
    build_regional_ids_dict()
    build_dex_desc_dict()

    # parses dex entries
    with open(dex_entries_file, 'r', encoding='utf-8') as f:
        file_content = f.read()

        # pattern to match every entry data block
        pattern = re.compile(r'\[(\w+)\]\s*=\s*\{\s*(.*?)\s*\},', re.DOTALL)

        # pattern to match each item property
        property_pattern = re.compile(r'\.(\w+)\s*=\s*([^,]+),')

        for match in pattern.finditer(file_content):
            national_id = match.group(1)
            regional_id = re.sub(r'NATIONAL', 'HOENN', national_id)
            species_id = re.sub(r'NATIONAL_DEX_', '', national_id)
            entry_properties = match.group(2)

            properties = {}

            # adds misssing fields
            properties['species'] = species_names_dict[species_id]
            properties['national_id'] = int(national_ids_dict[national_id])
            properties['regional_id'] = int(regional_ids_dict.get(regional_id, 0))

            for prop_match in property_pattern.finditer(entry_properties):
                key = prop_match.group(1)
                value = prop_match.group(2)

                if value.isdigit():
                    value = int(value)
                elif value == 'TRUE':
                    value = True
                elif value == 'FALSE':
                    value = False

                # reformats field names
                if key == 'categoryName':
                    key = 'category_name'
                    value = re.sub(r'\_\("|"\)', '', value)
                elif key == 'description':
                    value = dex_desc_dict[value]
                elif key in ignored_fields: # discards ignored fields
                    continue

                properties[key] = value

            dex_entries_dict[national_id] = properties

        for key, value in dex_entries_dict.items():
            json_dex_entries_list.append(value)
    
        return json_dex_entries_list
