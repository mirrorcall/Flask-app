"""
    This file is going to automatically insert json recipes into posgresql database
"""
import os
import json
import re

import psycopg2


# change postgres server at the beginning
conn = psycopg2.connect(database="planner", user="postgres",
                        password="mirrorcall", host="localhost",
                        port="5433")
cur = conn.cursor()


def correct_data(data):
    new = str(data).replace("'", "''")
    re.sub('\\[\w]*', '', new)

    return new.strip()


def create_table():
    global conn
    global cur

    sql = 'CREATE TABLE recipe_category (' \
        'rcid SERIAL4 PRIMARY KEY,' \
        'rc_name VARCHAR' \
        ');' \
        'CREATE TABLE recipe (' \
        '	rid SERIAL4 PRIMARY KEY,' \
        '	r_name VARCHAR NOT NULL,' \
        '	r_description VARCHAR DEFAULT \'none\',' \
        '   r_img VARCHAR DEFAULT \'none\',' \
        '   r_url VARCHAR NOT NULL,' \
        '	i_ids INTEGER[],' \
        '	rc_ids INTEGER[]' \
        ');'
    cur.execute(sql)


def drop_table():
    global conn
    global cur

    sql = 'DROP TABLE IF EXISTS recipe_category CASCADE;DROP TABLE IF EXISTS recipe CASCADE;'
    cur.execute(sql)


def query_ingre_id(ingre):
    global conn
    global cur

    sql = 'SELECT * FROM ingredient WHERE i_name = \'%s\'' % correct_data(ingre)
    cur.execute(sql)
    rs = cur.fetchone()
    return int(rs[0])


def list_to_array(alist):
    var = '{'
    i = 1

    if len(alist) == 0:
        return '{}'

    for x in alist:
        if i == len(alist):
            var += str(x) + '}'
        else:
            var += str(x) + ','
        i += 1

    return var


def check_ingre_id(item):
    idlist = []
    for i in item:
        idlist.append(query_ingre_id(i))

    array = list_to_array(idlist)

    return array


def insert_into_reci(item):

    for x in range(len(item)):
        sql = 'INSERT INTO recipe (r_name, r_description, r_img, r_url, i_ids)' \
              'VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % (correct_data(item[x]['title']),
                                                           correct_data(item[x]['description']),
                                                           correct_data(item[x]['img']),
                                                           correct_data(item[x]['url']),
                                                           check_ingre_id(item[x]['ingredients-matched']))
        cur.execute(sql)
        #print(x)



def main():
    global conn
    global cur

    drop_table()
    create_table()

    for dirpath, dirnames, files in os.walk('./recipes_JSON'):
        for f in files:
            if f == '.DS_Store':
                pass
            else:
                with open('recipes_JSON/'+f) as data_file:
                    data = json.load(data_file)
                    #print(len(data['recipes']))
                    #print(correct_data(data['recipes'][0]))
                    insert_into_reci(data['recipes'])

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()