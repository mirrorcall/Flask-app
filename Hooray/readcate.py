"""
    This file is going to automatically insert category data in to postgresql database
"""

import json
import pprint


with open('JSON/Arborio Rice.json') as f:
    data = json.load(f)

    array = '{'

    for x in range(0, len(data['categories'])):

        if x == len(data['categories'])-1:
            array += str(data["categories"][x]) + '}'
        else:
            array += str(data["categories"][x]) + ', '

    print(array)