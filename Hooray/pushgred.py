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
    sql = 'DROP TABLE IF EXISTS ingredient_category CASCADE;DROP TABLE IF EXISTS ingredient CASCADE;'
    cur.execute(sql)


def create_table():
    global conn
    global cur

    sql = 'CREATE TABLE ingredient_category (' \
          'icid SERIAL4,' \
          'ic_name VARCHAR UNIQUE NOT NULL,' \
          'PRIMARY KEY (icid)' \
          ');' \
          'CREATE TABLE ingredient (' \
          'iid SERIAL4,' \
          'i_name VARCHAR UNIQUE NOT NULL,' \
          'ic_ids INTEGER[],' \
          'alt_names TEXT[],' \
          'PRIMARY KEY (iid)' \
          ');'
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

    sql = "INSERT INTO ingredient (i_name, ic_ids, alt_names)" \
          "SELECT \'%s\', \'%s\', \'%s\'" \
          "WHERE NOT EXISTS (SELECT iid FROM ingredient WHERE i_name = \'%s\')" \
          "RETURNING iid" % (correct_data(item["name"]), build_array(select_ingre_cate(item)), build_array(item["altnames"]), correct_data(item["name"]))
    cur.execute(sql)
    print(sql)


# param: primitive json file data
def select_ingre_cate(item):
    global conn
    global cur

    mylist = []

    for x in range(0, len(item['categories'])):
        sql = "SELECT icid FROM ingredient_category WHERE ic_name = \'%s\'" % (correct_data(item['categories'][x]))
        cur.execute(sql)

        rs = cur.fetchone()
        mylist.append(rs[0])

    return mylist


def build_array(array):
    var = '{'
    i = 1

    if len(array) == 0:
        return '{}'

    for x in array:

        if i == len(array):
            var += correct_data(x) + '}'
        else:
            var += correct_data(x) + ', '
        i += 1

    #print(var)
    return var


def update_ingre_cate(ic_name):
    global conn
    global cur


def main():
    global conn
    global cur

    # rebuild the database every time running script
    drop_table()
    create_table()

    # walking through all files in JSON directories
    for dirpath, dirnames, files in os.walk('./ingredients_JSON'):
        for f in files:
            if f == '.DS_Store':
                pass
            else:
                with open('ingredients_JSON/'+f) as data_file:
                    data = json.load(data_file)
                    insert_into_cate(data)
                    insert_into_ingre(data)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()