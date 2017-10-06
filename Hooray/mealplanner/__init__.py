from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from mealplanner import models


app = Flask(__name__)

app.config.from_object('config')


@app.route('/')
def main():
    return 'Hello World!'

db = SQLAlchemy(app)
db.init_app(app)
