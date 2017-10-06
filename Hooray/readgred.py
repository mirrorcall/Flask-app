"""
    This file is going to automatically insert json ingredients into posgresql database
"""


import os
import json
import psycopg2


conn = psycopg2.connect(database="planner", user="postgres",
                        password="mirrorcall", host="localhost",
                        port="5433")
cur = conn.cursor()


def correct_data(data):
    return str(data).replace("'", "''")


def insert_into_db(item):
    global conn
    global cur

    sql = "INSERT INTO ingredients (i_name) VALUES (\'%s\')" % correct_data(item["name"])

    cur.execute(sql)


def insert_into_cate(item):
    global conn
    global cur




def main():
    global conn
    global cur

    # walking through all files in JSON directories
    for dirpath, dirnames, files in os.walk('./JSON'):
        for f in files:
            if f == '.DS_Store':
                pass
            else:
                with open('JSON/'+f) as data_file:
                    data = json.load(data_file)
                    insert_into_db(data)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()