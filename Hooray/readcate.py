"""
    This file is going to automatically insert category data in to postgresql database
"""

import json
import pprint

with open('JSON/Arborio Rice.json') as f:
    data = json.load(f)

    for x in range(0, len(data['categories'])):
        sql = "INSERT INTO ingredient_category (c_name) VALUES (\'%s\')" % (data['categories'][x])
        print(sql)