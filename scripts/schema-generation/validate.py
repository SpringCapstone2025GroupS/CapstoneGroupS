"""
This script is to test that the modified model does not error on the collected data.
"""

import os
from typing import Any, List

from pydantic import ValidationError
from .model_modified import APIResponseSuccess 


COLLECTION_DIR = os.path.join(os.path.dirname(__file__), "collected")


# Combine for Quicktype
response = {}
NOTAMitems : List[dict[str, Any]] = []
for file in os.listdir(COLLECTION_DIR):
    path = f"{COLLECTION_DIR}/{file}"
    with open(path, 'r') as file:
        try:
            response = APIResponseSuccess.model_validate_json(file.read())
        except ValidationError as e:
            print(f"Failed Validation on {file}")
            raise