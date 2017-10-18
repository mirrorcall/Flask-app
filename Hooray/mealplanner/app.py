import re

from flask_sqlalchemy import SQLAlchemy
#from mealplanner import models_food
from flask import Flask, redirect, render_template, json, request, jsonify, url_for, session
from mealplanner.forms import SearchForm
import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy import Table, Column, Integer, String, ForeignKey
import pandas as pd
import sys


app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
db.init_app(app)

# The return value of create_engine() is our connection object
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], client_encoding='utf8')


'''
if not con.dialect.has_table(con, 'recipe'):  # If table don't exist, Create.
    recipe = Table('recipe', meta,
			   Column('id', Integer, primary_key=True),
			   Column('name', String), 
    		   Column('description', String), 
			   Column('steps', String)
			   )

    ingredients = Table('ingredients', meta,
	    				Column('recipeid', Integer, ForeignKey('recipe.id')), 
		    			Column('ingredient', String)
			    		)

    #create above tables
    meta.create_all(con)
'''
toInsert = [
    {'id': 1, 'name': 'chocolate cake', 'description': 'this is chocolate cake', 'steps': '1. mix ingredients 2.bake'}
]
# con.execute(meta.tables['recipe'].insert(), toInsert)

toInsert = [
    {'recipeid': 1, 'ingredient': 'flour'},
    {'recipeid': 1, 'ingredient': 'cocoa'},
    {'recipeid': 1, 'ingredient': '3 eggs'},
    {'recipeid': 1, 'ingredient': 'butter'}
]


# con.execute(meta.tables['ingredients'].insert(), toInsert)



# main page
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        print('if', file=sys.stderr)
        try:
            form = SearchForm()
            _query = request.form['query']
            return redirect(url_for('result', query=_query))
        except Exception as e:
            form = SearchForm()
            return render_template('index.html',
                                   title='Home',
                                   form=form)


    else:
        print('else', file=sys.stderr)
        form = SearchForm()
        # if form.validate_on_submit():
        #    flash('Search requested for query="%s"' %
        #          (form.query.data))
        #    return redirect(url_for('result', query=form.query.data), evidence=form.evidence.data)
        return render_template('index.html',
                               title='Search',
                               form=form)
    return render_template('index.html')


# result page
@app.route('/result/<query>', methods=['GET', 'POST'])
def result(query):
    q = text("Select * from ingredient where i_name like :i")
    result = engine.execute(q, i=query).fetchall()
    print(result)
    resultset = [dict(row) for row in result]
    df = pd.DataFrame(data=result, columns=['iid', 'i_name', 'i_description', 'ic_id'])
    print(df)
    print(resultset)
    form = SearchForm()
    return render_template('result.html',
                           title='Results',
                           form=form, data=df.to_html())


"""
    :param query    str type that can be any case and return the top 5 result in json format
"""


#@app.route('/autocomplete/<query>', methods=['GET'])
#def autocomplete(query):
#    # remove all the non-alphabet chars
#    query = str.lower(str(query))
#    re.sub(r'[^a-zA-Z]', '', query)
#    unique_list = []
#    result = []
#    conn = engine.connect()
#    sql = 'SELECT i.* FROM ingredient i, UNNEST(alt_names) names WHERE (lower(i_name) LIKE \'%s%s%s\') OR ' \
#          '(lower(names) LIKE \'%s%s%s\') ORDER BY iid ASC LIMIT 100' % ('%', query, '%', '%', query, '%')
#    rs = conn.execute(sqlalchemy.text(sql))
#    for row in rs:
#        if row['i_name'] not in unique_list:
#            unique_list.append(row['i_name'])
#            result.append(row)
#            print(row)
#        if len(unique_list) == 5:
#            break

#    rs.close()

#    df = pd.DataFrame(data=result, columns=['ingredient_id', 'ingredient_name', 'ingredient_category', 'alt-name'])
#    print(df)




@app.route('/autocomplete',methods=['GET'])
def autocomplete():

    search = request.args.get('q')
    conn = engine.connect()
    #cursor = conn.cursor()
    sql="select i_name from ingredient where i_name like '%"+search+"%'"
    rs=conn.execute(sqlalchemy.text(sql))
    symbols = rs.fetchall()
    results = [mv[0] for mv in symbols]
    print(results)
    
    #cursor.close()
    conn.close()


    return jsonify(matching_results=results)

@app.route('/signUpUser', methods = ['GET','POST'])
def signUpUser():
    conn = engine.connect()
    sql = "SELECT * FROM users WHERE users.u_email='%s'" % (request.form['inputEmail'])
    result = conn.execute(sql).fetchall()
    if len(result) < 1:
        sql = "INSERT INTO users (u_name,u_email,u_password) VALUES ('%s','%s','%s');" % (request.form['inputName'],request.form['inputEmail'],request.form['inputPassword'])
        conn.execute(sql)
    return redirect(url_for('main'))

@app.route('/signUp', methods = ['GET','POST'])
def signUp():      
    return render_template('signup.html', title= 'Sign Up')

@app.route('/signInUser', methods = ['GET','POST'])
def signInUser():
    conn = engine.connect()
    sql = "SELECT * FROM users WHERE users.u_email='%s' AND users.u_password='%s';" % (request.form['inputEmail'],request.form['inputPassword'])
    result = conn.execute(sql).fetchall()
    if len(result) == 1 and not 'userEmail' in session:
        session['userEmail'] = request.form['inputEmail']

    return redirect(url_for('main'))

@app.route('/signIn', methods = ['GET','POST'])
def signIn():      
    return render_template('signin.html', title= 'Sign In')

@app.route('/signOut', methods = ['GET','POST'])
def signOut():
    if 'userEmail' in session:
        session.pop('userEmail')
    return redirect(url_for('main'))

app.secret_key = 'hooray'
