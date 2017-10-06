"""
    This file is going to automatically insert category data in to postgresql database
"""

import json
import pprint

with open('JSON/Arborio Rice.json') as f:
    data = json.load(f)
    print(len(data["categories"][0]['run']))