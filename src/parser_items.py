# Parses items from the game source code and writes them to a JSON file.
# An item has the following fields:
# - item_id             the item's id
# - name:               the item's name
# - description:        the item's description
# - pocket:             the item's pocket
# - type:               the item's type
# - price:              the item's price
# - hold_effect:        the item's hold effect
# - hold_effect_arg:    the item's hold effect argument
# - battle_usage:       the item's battle usage
# - secondary_id:       the item's secondary id
# - importance:?????    the item's importance (used to avoid item tossing)
#                       -> value can be (0, 1, 2) but game only checks for 0 and != 0, so 2 seems to be pointless

import re
import resource_manager as rm

item_ids_dict = {}          # ITEM_XXX --> id
item_desc_dict = {}         # sMoveDescXXX --> "description text"
item_pockets_dict = {}      # POCKET_XXX --> pocket
item_types_dict = {}        # ITEM_USE_XXX --> type
hold_effects_dict = {}      # HOLD_EFFECT_XXX --> hold effect
battle_usages_dict = {}     # ITEM_B_USE_XXX --> battle usage
named_mt_to_mt_dict = {}    # ITEM_TMXX_XXX --> ITEM_TMXXX

# builds a dictionary with item ids and their numbers (ITEM_XXX, 0)
def build_item_ids_dict():
    with open(rm.item_ids_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define (ITEM_\w+)\s+(\d+)', line)
            if match:
                mcheck1 = re.match(r'ITEM_USE_\w+', match.group(1))
                mcheck2 = re.match(r'ITEM_B_USE_\w+', match.group(1))
                # avoids parsing ITEM_USE_XXX and ITEM_B_USE_XXX
                if mcheck1 or mcheck2: 
                    continue
                # creates an item entry
                key = match.group(1)
                value = match.group(2)
                item_ids_dict[key] = value

# builds a dictionary sMoveDescXXX --> "description text"
def build_items_desc_dict():
    with open(rm.item_desc_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

        pattern = r'static\s+const\s+u8\s+(s\w+)\[\]\s+=\s+_\(\s*"((?:.|\n)*?)"\);'
        matches = re.findall(pattern, file_content)

        for match in matches:
            id = match[0]
            desc = re.sub(r'\\n|"|\t', '', match[1])    # replaces \n, " and \t with ''
            desc = re.sub(r'\n', ' ', desc)             # replaces \n with ' '
            desc = re.sub(r'\s+', ' ', desc)            # replaces multiple spaces with a single space
            desc = re.sub(r'-\s+', '', desc)            # replaces '-' followed by a space with ''
            item_desc_dict[id] = desc
        
# builds a dictionary with item pockets (POCKET_XXX, pocket)
def build_items_pockets_dict():
    with open(rm.item_pockets_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define\s+(POCKET_\w+)\s+\d+', line)
            if match:
                key = match.group(1)
                value = re.sub(r'POCKET_', '', key)
                value = value.lower()
                item_pockets_dict[key] = value

# builds a dictionary with item types (ITEM_USE_XXX, type)
def build_item_types_dict():
    with open(rm.item_types_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define\s+(ITEM_USE_\w+)\s+\d+', line)
            if match:
                key = match.group(1)
                value = re.sub(r'ITEM_USE_', '', key)
                value = value.lower()
                item_types_dict[key] = value

# builds a dictionary with hold effects (HOLD_EFFECT_XXX, hold effect)
def build_hold_effects_dict():
    with open(rm.hold_effects_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define\s+(HOLD_EFFECT_\w+)\s+\d+', line)
            if match:
                key = match.group(1)
                value = re.sub(r'HOLD_EFFECT_', '', key)
                value = value.lower()
                hold_effects_dict[key] = value

# builds a dictionary with battle usages (ITEM_B_USE_XXX, battle usage)
def build_battle_usages_dict():
    with open(rm.battle_usages_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define\s+(ITEM_B_USE_\w+)\s+\d+', line)
            if match:
                key = match.group(1)
                value = re.sub(r'ITEM_B_USE_', '', key)
                value = value.lower()
                battle_usages_dict[key] = value

# builds a dictionary with named TM/HM items to numbered TM/HM items (ITEM_TMXX_XXX, ITEM_TMXXX)
def build_named_mt_to_mt_dict():
    with open(rm.item_ids_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define\s+(ITEM_TM\d+_\w+)\s+(\w+)', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                named_mt_to_mt_dict[key] = value
            match = re.match(r'#define\s+(ITEM_HM\d+_\w+)\s+(\w+)', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                named_mt_to_mt_dict[key] = value

# tries to fixe named TM/HM items to numbered TM/HM items: ITEM_TM01_FLAMETHROWER --> ITEM_TM01
def try_fix_named_tm_hm(item_id):
    if (re.match(r'ITEM_TM\d+_\w+', item_id)) or (re.match(r'ITEM_HM\d+_\w+', item_id)):
        item_id = named_mt_to_mt_dict[item_id]
    return item_id

# parses items from the game source code and returns a list of items in JSON format
def parse_to_json(items_file):

    items_dict = {}
    json_items_list = []

    # TODO: externalize into config file
    item_fields_order = ["item_id", 'name', "description", "pocket", "type", "price", "hold_effect", "hold_effect_arg", "battle_usage", 'secondary_id', 'importance']

    build_item_ids_dict()
    build_items_desc_dict()
    build_items_pockets_dict()
    build_item_types_dict()
    build_hold_effects_dict()
    build_battle_usages_dict()
    build_named_mt_to_mt_dict()
    #fix_dict_item_tm_hm(item_ids_dict)

    # parses items
    with open(items_file, 'r', encoding='utf-8') as f:
        file_content = f.read()

        # pattern to match every item data block
        pattern = re.compile(r'\[(\w+)\]\s*=\s*\{\s*(.*?)\s*\},', re.DOTALL)

        # pattern to match each item property
        property_pattern = re.compile(r'\.(\w+)\s*=\s*([^,]+),')

        for match in pattern.finditer(file_content):
            
            item_id = match.group(1)
            item_properties = match.group(2)
            
            # fixes named TM/HM items to numbered TM/HM items
            if (re.match(r'ITEM_TM\d+_\w+', item_id)) or (re.match(r'ITEM_HM\d+_\w+', item_id)):
                item_id = named_mt_to_mt_dict[item_id]
            
            properties = {}
            
            for prop_match in property_pattern.finditer(item_properties):
                key = prop_match.group(1)
                value = prop_match.group(2)

                if value.isdigit():
                    value = int(value)
                elif value == 'TRUE':
                    value = True
                elif value == 'FALSE':
                    value = False

                if key == 'name':
                    value = re.sub(r'\_\("|"\)', '', value)
                elif key == 'itemId':
                    value = item_ids_dict[try_fix_named_tm_hm(value)]
                    key = 'item_id'
                elif key == 'description':
                    value = item_desc_dict[value]
                elif key == 'pocket':
                    value = item_pockets_dict[value]
                elif key == 'type':
                    value = item_types_dict[value]
                elif key == 'holdEffect':
                    if value == 0:
                        value = 'none'
                    else:
                        value = hold_effects_dict[value]
                    key = 'hold_effect'
                elif key == 'battleUsage':
                    value = battle_usages_dict[value]
                    key = 'battle_usage'
                elif key == 'secondaryId':
                    if isinstance(value, str):
                        value = value.lower()
                    key = 'secondary_id'
                elif key == 'fieldUseFunc' or key == 'battleUseFunc':
                    continue

                properties[key] = value

            ordered_properties = {key: properties.get(key, "none" if key == 'hold_effect' or key == 'battle_usage' else 0) for key in item_fields_order}

            items_dict[item_id] = ordered_properties

        for item_name, item_data in items_dict.items():
            json_items_list.append(item_data)
        
        return json_items_list
