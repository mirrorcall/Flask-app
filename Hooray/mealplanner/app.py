from flask_sqlalchemy import SQLAlchemy
# from mealplanner import models generate circular import - import error
from flask import Flask, redirect, render_template, json, request, jsonify, url_for
from mealplanner.forms import SearchForm
import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy import Table, Column, Integer, String, ForeignKey
import pandas as pd


app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
db.init_app(app)


def connect():
    '''Returns a connection and a metadata object'''
    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta


con, meta = connect()
con
meta

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
    q = text("Select * from recipe where id in (Select recipeid from ingredients where ingredient like :i)")
    result = con.execute(q, i=query).fetchall()
    print(result)
    resultset = [dict(row) for row in result]
    df = pd.DataFrame(data=result, columns=['id', 'name', 'description', 'steps'])
    print(df)
    print(resultset)
    form = SearchForm()
    return render_template('result.html',
                           title='Results',
                           form=form, data=df.to_html())

'''
if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True)
    app.run(debug=True)
'''