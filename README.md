# Hooray - Meal planner

Simple flask web deployment with connecting to postgresql

**CHECK CONNFIG.PY FIRST MAKE SURE IT MATCHES YOUR LOCAL POSTGRES SERVER**

------

### Env require:

* flask
* flask_migrate
* flask_script
* flask_sqlalchemy
* flask_wtf
* psycopg2
* pandas
* sqlalchemy

download python package with command `sudo pip3 install <package-name>`

------

### Database:

**Design**

Table 1):
1. planner.recipes holds primary key rid, r\_name as recipes' name, r\_description

> Description

Column     |       Type        |                       Modifiers                       | Storage  | Stats target | Description
---------------+-------------------+-------------------------------------------------------+----------+--------------+-------------
 rid           | integer           | not null default nextval('recipes_rid_seq'::regclass) | plain    |              |
 r_name        | character varying |                                                       | extended |              |
 r_description | character varying |                                                       | extended |              |

2. planner.ingredients holdes primary key iid, i\_name as ingredients' name, i_description as specific quality and quantity and foreign key r\_id refering to *rid* in recipes

> Description

Column     |       Type        |                         Modifiers                         | Storage  | Stats target | Description
---------------+-------------------+-----------------------------------------------------------+----------+--------------+-------------
 iid           | integer           | not null default nextval('ingredients_iid_seq'::regclass) | plain    |              |
 i_name        | character varying |                                                           | extended |              |
 i_description | character varying |                                                           | extended |              |
 r_id          | integer           |                                                           | plain    |              |
Indexes:
    "ingredients_pkey" PRIMARY KEY, btree (iid)
Foreign-key constraints:
    "ingredients_r_id_fkey" FOREIGN KEY (r_id) REFERENCES recipes(rid)

3. planner.steps holds primary key sid, s\_name as steps' name, s\_detail as specific operation in ingredients, r\_id refering to *rid* in recipes

> Description

Column  |       Type        |                      Modifiers                      | Storage  | Stats target | Description
----------+-------------------+-----------------------------------------------------+----------+--------------+-------------
 sid      | integer           | not null default nextval('steps_sid_seq'::regclass) | plain    |              |
 s_name   | character varying |                                                     | extended |              |
 s_detail | character varying |                                                     | extended |              |
 r_id     | integer           |                                                     | plain    |              |
Indexes:
    "steps_pkey" PRIMARY KEY, btree (sid)
Foreign-key constraints:
    "steps_r_id_fkey" FOREIGN KEY (r_id) REFERENCES recipes(rid)

To create the database:

running `python3 createdb`


**Migration**

Hooray/mealplanner/migrations contains the migrating database configurations

```python3
# Initialising
python3 manager.py db init

# Generate migrations (running only ONCE)
python3 manager.py db migrate

# Generate new migration in migrations folder
python3 manager.py db upgrade
```
