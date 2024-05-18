# Parses growth rates from the game source code and writes them to a JSON file.
# a growth rate has the following fields:
# - id:             the growth rate's id
# - growth_type:    the growth rate's name
# - formula:        the growth rate's formula
# - max_exp:        the growth rate's max experience

# TODO: consider the possibility of putting formulas as an array, so we can have multiple formulas for the same growth rate

import re
import resource_manager as rm

growth_rates_ids_dict = {}      # GROWTH_XXXXX: id
growth_rates_names_dict = {}    # GROWTH_XXXXX: name

# growth rate formulas ----> GROWTH_XXXXX: formula
GROWTH_RATE_FORMULAS = {
    "GROWTH_MEDIUM_FAST": "n^3",
    "GROWTH_ERRATIC"    : """((n^3)(100 - n))/50 if n < 50
((n^3)(150 - n))/100 if 50 < n < 68
((n^3)((1911 - 10n)/3))/500 if 68 < n < 98
((n^3)(160 - n))/100 if 98 < n < 100""",
    "GROWTH_FLUCTUATING": """((n^3)((24 + ((n + 1)/3))/50 if n < 15
((n^3)((14 + n)/50 if 15 < n < 36
((n^3)((32 + n/2)/50 if 36 < n < 100""",
    "GROWTH_MEDIUM_SLOW": "(6/5)n^3 - 15n^2 + 100n - 140",
    "GROWTH_FAST"       : "(4n^3)/5",
    "GROWTH_SLOW"       : "(5n^3)/4"
}

# growth rate max experience ----> GROWTH_XXXXX: max_exp
GROWTH_RATE_MAX_EXP = {
    "GROWTH_MEDIUM_FAST": 1000000,
    "GROWTH_ERRATIC"    : 600000,
    "GROWTH_FLUCTUATING": 1640000,
    "GROWTH_MEDIUM_SLOW": 1059860,
    "GROWTH_FAST"       : 800000,
    "GROWTH_SLOW"       : 1250000
}

# builds a dictionary with growth rates ids
def build_growth_rates_ids_dict():
    with open(rm.growth_rates_ids_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'#define (GROWTH_\w+)\s+(\d+)', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                growth_rates_ids_dict[value] = key

# builds a dictionary with growth rates names
def build_growth_rates_names_dict():
    for key, value in growth_rates_ids_dict.items():
        name = re.sub(r'GROWTH_', '', value)
        name = name.lower()
        growth_rates_names_dict[value] = name

# parses growth rates to a JSON file
def parse_to_json():
    growth_rates_dict = {}
    json_growth_rates_list = []

    build_growth_rates_ids_dict()
    build_growth_rates_names_dict()

    for key, value in growth_rates_ids_dict.items():
        growth_rates_dict['id'] = key
        growth_rates_dict['name'] = growth_rates_names_dict[value]
        growth_rates_dict['formula'] = GROWTH_RATE_FORMULAS[value]
        growth_rates_dict['max_exp'] = GROWTH_RATE_MAX_EXP[value]
        json_growth_rates_list.append(growth_rates_dict.copy())

    return json_growth_rates_list
