import os
import json
import re

import psycopg2

# change postgres server at the beginning
conn = psycopg2.connect(database="recipe", user="postgres",
                        password="Sharon0108", host="localhost",
                        port="5432")
cur = conn.cursor()

def main():
    global conn
    global curr

    sql = "CREATE TABLE users (uid SERIAL4 PRIMARY KEY,u_name VARCHAR NOT NULL,u_email VARCHAR UNIQUE NOT NULL, u_password VARCHAR NOT NULL);"
    cur.execute(sql)

    conn.commit()

if __name__ == '__main__':
    main()
