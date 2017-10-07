# Hooray - Meal planner

Simple flask web deployment with connecting to postgresql

**CHECK CONNFIG.PY FIRST MAKE SURE IT MATCHES YOUR LOCAL POSTGRES SERVER**

------

### Dependency Installation:

```
pip3 install -r requirements.txt
```


------

### Database:

**Initialisation**

```
python3 createdb.py
```

**Populating JSON files**

```
python3 pushgred.py
```

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
