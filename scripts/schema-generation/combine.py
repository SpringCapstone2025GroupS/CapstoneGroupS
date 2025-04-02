"""
Combines the responses saved in ./collected/ into one JSON file to use with Quicktype
"""
import os
import json
from typing import Any, List

# Combine for Quicktype
response = {}
NOTAMitems : List[dict[str, Any]] = []
for file in os.listdir("./scripts/data-for-schema-generation/collected/"):
    with open(f"./scripts/data-for-schema-generation/collected/{file}", 'r') as file:
        response = json.load(file)
        NOTAMitems.extend(response.get("items", []))

    
with open(f'./scripts/data-for-schema-generation/quicktype_input.json', 'w') as file:
    response["items"] = NOTAMitems
    json.dump(response, file)
