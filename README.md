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

download python3 package with command `sudo pip3 install <package-name>`

------

### Database:

**Design**

Table 1):
1. planner.recipes holds primary key rid, r\_name as recipes' name, r\_description

2. planner.ingredients holdes primary key iid, i\_name as ingredients' name, i_description as specific quality and quantity and foreign key r\_id refering to *rid* in recipes

3. planner.steps holds primary key sid, s\_name as steps' name, s\_detail as specific operation in ingredients, r\_id refering to *rid* in recipes


To create the database:

running `python3 createdb.py`


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
