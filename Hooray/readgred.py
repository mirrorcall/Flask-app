"""
    This file is going to automatically insert json ingredients into posgresql database
"""
import os
import json
import psycopg2


# change postgres server at the beginning
conn = psycopg2.connect(database="planner", user="postgres",
                        password="mirrorcall", host="localhost",
                        port="5433")
cur = conn.cursor()


def correct_data(data):
    return str(data).replace("'", "''")


def drop_table():
    sql = "DROP TABLE IF EXISTS ingredient_category;DROP TABLE IF EXISTS ingredients;"
    cur.execute(sql)


# insertion only happens when the data not exist
def insert_into_cate(item):
    global conn
    global cur

    for x in range(0, len(item['categories'])):
        sql = "INSERT INTO ingredient_category (ic_name)" \
              "SELECT \'%s\'" \
              "WHERE NOT EXISTS (SELECT icid FROM ingredient_category WHERE ic_name = \'%s\')" \
              "RETURNING icid" % (correct_data(item['categories'][x]), correct_data(item['categories'][x]))
        cur.execute(sql)


# insertion only happens when the data not exist
def insert_into_ingre(item):
    global conn
    global cur

    sql = "INSERT INTO ingredient (i_name)" \
          "SELECT \'%s\'" \
          "WHERE NOT EXISTS (SELECT iid FROM ingredient WHERE i_name = \'%s\')" \
          "RETURNING iid" % (correct_data(item["name"]), correct_data(item["name"]))
    cur.execute(sql)


def main():
    global conn
    global cur

    # rebuild the database every time running script
    # drop_table()

    # walking through all files in JSON directories
    for dirpath, dirnames, files in os.walk('./JSON'):
        for f in files:
            if f == '.DS_Store':
                pass
            else:
                with open('JSON/'+f) as data_file:
                    data = json.load(data_file)
                    insert_into_ingre(data)
                    insert_into_cate(data)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()