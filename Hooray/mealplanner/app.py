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
@app.route('/<tags>', methods=['GET', 'POST'])
def main(tags=None): 
    #alltags2=[]
    #newtags2=[]
    tagarray=[]
    gettags = tags
    #print(tags)
    #print('HUDWHIHD')
    if tags != None:
        #alltags2.extend([tags])
        tagarray=gettags.split(",")
        #gettagsfix = re.search("'.*'", gettags, flags =0).group()
        #gettagsfix = re.sub("'", '', gettagsfix)
        #stringtags = ''.join(alltags2)
        tagarray= [re.search("'.*'", elem, flags=0).group() for elem in tagarray]
        tagarray= [re.sub("'", '', elem) for elem in tagarray]
        #newtags2.extend([gettagsfix])
        #stringtags = re.sub(']', '', stringtags)
        #stringtags = re.sub('[', '', stringtags)
        
        #stringt2 = re.sub("'", '', stringt.group())
        #print('string')
        
        #print(tagarray)
       # print('stringend')
    if request.method == 'POST':
        print('if', file=sys.stderr)
        _query = request.form['query']
        #print('query')
        #print(_query)
        if request.form['submit'] == 'Search':
            try:
                form = SearchForm()
                #_query = request.form['query']
                return redirect(url_for('result', query=_query))
            except Exception as e:
                form = SearchForm()
                return render_template('index.html',
                                       title='Home',
                                       form=form)

        if request.form['submit'] == 'Add':
            #print('1')
            tagarray.append(_query)
            #print(tagarray)
            for tag in tagarray:
                print(tag)
            try:
                form = SearchForm()
                #_query = request.form['query']
                #tags.append(_query)
                return redirect(url_for('main', tags=tagarray))
                #return render_template('index.html',
                #                       title='Home',
                #                       form=form, tags=_query)

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
                               form=form, tags=tagarray)
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
    :param      query    str type that can be any case
    :return     df       the top 5 result in json format
"""


@app.route('/autocomplete',methods=['GET'])
def autocomplete():
    # remove all the non-alphabet chars
    query = request.args.get('q')
    query = str.lower(str(query))
    re.sub(r'[^a-zA-Z]', '', query)
    ingredients = dict()
    unique_list = []
    results = []
    conn = engine.connect()
    sql = 'SELECT i.* FROM ingredient i, UNNEST(alt_names) names WHERE (lower(i_name) LIKE \'%s%s%s\') OR ' \
          '(lower(names) LIKE \'%s%s%s\') ORDER BY iid ASC LIMIT 100' % ('%', query, '%', '%', query, '%')
    rs = conn.execute(sqlalchemy.text(sql))
    for row in rs:
        if row['i_name'] not in unique_list:
            unique_list.append(row['i_name'])
            results.append(row)

        if len(unique_list) == 5:
            break

    rs.close()

    for res in results:
        if query in str.lower(res['i_name']):
            ingredients[res['iid']] = res['i_name']
        else:
            for x in res['alt_names']:
                if query in str.lower(x):
                    ingredients[res['iid']] = x

    print(json.dumps(ingredients))

    df = pd.DataFrame(data=results, columns=['ingredient_id', 'ingredient_name', 'ingredient_category', 'alt-name'])
    #print(df)



def init_array(query):
    alist = query.split('-')[:]
    parray = 'ARRAY['
    i = 1
    for x in alist:
        if i == len(alist):
            parray += x + ']'
        else:
            parray += x + ','
        i += 1

    return str(parray)


"""
    :param      query    of str type (recipe title) or int type (ingredient id)
    :return        
"""
@app.route('/search_recipe/<query>', methods=['GET'])
def search_recipe(query):
    query = str.lower(str(query))
    re.sub(r'[^a-zA-Z]', '', query)
    conn = engine.connect()
    if re.search(r'\d', query):  # if query is digit check related ingredients id
        sql = "SELECT * FROM recipe WHERE %s <@ i_ids" % init_array(query)  # add LIMIT to restrict to specific # of output
    else:               # if query is alphabetic check recipes name
        sql = "SELECT * FROM recipe WHERE lower(r_name) LIKE \'%%%s%%\' ORDER BY rid" \
              % query  # add LIMIT to restrict to specific # of output
    rs = conn.execute(sqlalchemy.text(sql))
    for row in rs:
        print(row['r_name'])

    print(sql)

'''
@app.route('/autocomplete',methods=['GET'])
def autocomplete():

    search = request.args.get('q')
    conn = engine.connect()
    #cursor = conn.cursor()
    sql="select i_name from ingredient where i_name like '%"+search+"%' limit 10"
    rs=conn.execute(sqlalchemy.text(sql))
    symbols = rs.fetchall()
    results = [mv[0] for mv in symbols]
    print(results)
    
    #cursor.close()
    conn.close()


    return jsonify(matching_results=results)
'''

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
