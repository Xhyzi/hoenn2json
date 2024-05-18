import re
import resource_manager as rm

# dictionaries related to move data
move_ids_dict = {}      # MOVE_???? : id
move_names_dict = {}    # MOVE_???? : name
move_desc_dict = {}     # MOVE_???? : description
move_effect_dict = {}   # EFFECT_???? : effect
target_type_dict = {}   # MOVE_TARGET_???? : target_type
move_split_dict = {}    # SPLIT_???? : split
types_dict = {}         # TYPE_???? : type
move_effect2_dict = {}  # MOVE_EFFECT_???? : effect
move_flags_dict = {}    # FLAG_???? : flag

def fix_effect_value(effect):
    try:
        effect = move_effect2_dict[effect]
    except KeyError:
        if effect == "STATUS1_PARALYSIS":
            effect = "paralysis"
        elif effect == "STATUS1_SLEEP":
            effect = "sleep"
        elif effect == "STATUS1_BURN":
            effect = "burn"
        elif effect == "STATUS1_FREEZE":
            effect = "freeze"
        elif effect == "HOLD_EFFECT_PLATE":
            effect = "plate"
        elif effect == True:
            effect = "protect_whole_team"
        elif effect == "TYPE_FLYING":
            effect = "flying"
        elif effect == "TYPE_GHOST":
            effect = "ghost"
        elif effect == "TYPE_GRASS":
            effect = "grass"
        elif effect == "TYPE_PSYCHIC":
            effect = "psychic"
        elif effect == "HOLD_EFFECT_MEMORY":
            effect = "memory"
        elif effect == 75:
            effect = "75%"
        elif effect == 100:
            effect = "100%"
        else:
            print("Warning: Unknown move effect 2: ", effect)
    return effect

# builds move ids dictionary
def build_move_ids_dict():
    with open(rm.move_ids_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define\s+(MOVE_\w+)\s+(\d+)', line)
            if match:
                key = match.group(1)
                value = int(match.group(2))
                move_ids_dict[key] = value

# builds move names dictionary
def build_move_names_dict():
    with open(rm.move_names_path, 'r', encoding='utf-8') as f:
        for line in f:
            # (.+?) will take the shortest match
            match = re.match(r'\s+\[(MOVE_\w+)\]\s+=\s+_\("(.+?)"\)', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                move_names_dict[key] = value

# builds move descriptions dictionary
def build_desc_dictionary():
    with open(rm.move_desc_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

        pattern = r'static\sconst\su8\s(\w+)\[\]\s=\s_\(\s*"((?:.|\n)*?)"\);'
        matches = re.findall(pattern, file_content)

        tmp_id_desctxt_dict = {}

        for match in matches:
            id = match[0]
            desc = re.sub(r'\\n|"|\t', '', match[1])    # replaces \n and " with empty string
            desc = re.sub(r'\n', ' ', desc)             # replaces \n with space
            desc = re.sub(r'\s+', ' ', desc)            # replaces multiple spaces with single space
            tmp_id_desctxt_dict[id] = desc

        pattern = r'\s+\[(MOVE_\w+)\s+-\s+1\]\s+=\s+(s\w+),'
        matches = re.findall(pattern, file_content)

        for match in matches:
            move_desc_dict[match[0]] = tmp_id_desctxt_dict[match[1]]

# builds move effects dictionary
def build_move_effect_dict():
    with open(rm.move_effect_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define\s+(EFFECT_\w+)\s+(\d+)', line)
            if match:
                key = match.group(1)
                value = re.sub(r'EFFECT_', '', key).lower()
                move_effect_dict[key] = value

# builds the target type dictionary
def build_target_type_dict():
    with open(rm.battle_h_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

        pattern = r'#define\s+(MOVE_TARGET_\w+)\s+(0x[0-9A-Fa-f]+|[0-9A-Fa-f]+)'
        matches = re.findall(pattern, file_content)

        for match in matches:
            key = match[0]
            value = re.sub(r'MOVE_TARGET_', '', key).lower()
            target_type_dict[key] = value 

# builds the move split dictionary
def build_move_split_dict():
    with open(rm.pokemon_h_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

        pattern = r'#define\s+(SPLIT_\w+)\s+(0x[0-9A-Fa-f]+|[0-9A-Fa-f]+)'
        matches = re.findall(pattern, file_content)

        for match in matches:
            key = match[0]
            value = re.sub("SPLIT_", "", key).lower()
            move_split_dict[key] = value

# builds the types dictionary
def build_types_dict():
    with open(rm.pokemon_h_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

        pattern = r'#define\s+(TYPE_\w+)\s+(0x[0-9A-Fa-f]+|[0-9A-Fa-f]+)'
        matches = re.findall(pattern, file_content)
        
        for match in matches:
            types_dict[match[0]] = int(match[1], 0)

# builds the type names dictionary
def build_type_names_dict():
    with open(rm.type_names_file, 'r', encoding='utf-8') as f:
        file_content = f.read()
        pattern = r'const u8 gTypeNames\[\w+\]\[\w+ \+ 1\]\s*=\s*\{\s*((?:\s*_\(".*?"\),?\s*)+)\s*\};'
        match = re.search(pattern, file_content)
        type_names = []
        if match:
            block_content = match.group(1)
            text_pattern = r'_\("([^"]+)"\)'
            type_names = re.findall(text_pattern, block_content)
            return type_names
        else:
            print('Type names not found at file: ', rm.type_names_file)

# builds the move effects 2 dictionary 
def build_move_effects2_dict():
    with open(rm.move_effects2_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define\s+(MOVE_EFFECT_\w+)\s+(0x[0-9A-Fa-f]+|[0-9A-Fa-f]+)', line)
            if match:
                key = match.group(1)
                value = re.sub(r'MOVE_EFFECT_', '', key).lower()
                move_effect2_dict[key] = value

# builds the move flags dictionary
def build_move_flags_dict():
    with open(rm.move_flags_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define\s+(FLAG_\w+)\s+\(1\s+<<\s+(\d+)\)', line)
            if match:
                key = match.group(1)
                value = re.sub(r'FLAG_', '', key).lower()
                move_flags_dict[key] = value


def parse_to_json(moves_file):
    
    moves_dict = {}
    json_moves_list = []

    # TODO: externalize into config file
    move_fields_order = ["id", "name", "description", "type", "power", "accuracy", "pp", "priority", "split", "target", "effect", "effect_chance", "additional_effect", "flags"]
    
    build_move_ids_dict()
    build_move_names_dict()
    build_desc_dictionary()
    build_move_effect_dict()
    build_target_type_dict()
    build_move_split_dict()
    build_types_dict()
    types = build_type_names_dict()
    build_move_effects2_dict()
    build_move_flags_dict()

    # parses moves
    with open(moves_file, 'r', encoding='utf-8') as f:
        file_content = f.read()
        
        # pattern to extract every move data block
        pattern = re.compile(r'\[(\w+)\]\s*=\s*\{\s*(.*?)\s*\},', re.DOTALL)
        
        # pattern to extract each property from a move data block
        property_pattern = re.compile(r'\.(\w+)\s*=\s*([^,]+),')

        for match in pattern.finditer(file_content):
            if match.group(1) == 'MOVES_COUNT':
                continue

            move_name = match.group(1)
            move_properties = match.group(2)

            properties = {}
            properties["id"] = move_ids_dict[move_name]
            properties["name"] = move_names_dict[move_name]

            if "MOVE_MAX" in move_name or "MOVE_G_MAX" in move_name:
                properties["description"] = "TODO: No desc"
            else:
                properties["description"] = move_desc_dict[move_name]

            for prop_match in property_pattern.finditer(move_properties):
                key = prop_match.group(1)
                value = prop_match.group(2).strip()

                if value.isdigit():
                    value = int(value)
                elif value == 'TRUE':
                    value = True
                elif value == 'FALSE':
                    value = False

                # convert type to name
                if key == "effect":
                    value = move_effect_dict[value]
                elif key == "type":
                    value = types[types_dict[value]]
                elif key == "target":
                    target_list = value.split("|")
                    target_list = [target.strip() for target in target_list]
                    target_list = [target_type_dict[target] for target in target_list]
                    value = target_list
                elif key == "split":
                    value = move_split_dict[value]
                elif key == "argument":
                    value = fix_effect_value(value)
                elif key == "secondaryEffectChance":
                    key = "effect_chance"
                elif key == "flags" and value != 0:
                    flag_list = value.split("|")
                    flag_list = [flag.strip() for flag in flag_list]
                    flag_list = [move_flags_dict[flag] for flag in flag_list]
                    value = flag_list

                properties[key] = value

            # rearrange properties into the desired order
            ordered_properties = {k: properties[k] for k in move_fields_order if k in properties}
            
            moves_dict[move_name] = ordered_properties

        for move_name, move_data in moves_dict.items():
            json_moves_list.append(move_data)
        return json_moves_list

