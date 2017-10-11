from mealplanner.app import db
from sqlalchemy import ForeignKey


class BaseModel(db.Model):
    __abstract__ = True     # prevent from creating table for abstract model

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        return '%r(%r)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })


'''
class TableName(BaseModel, db.Model):
    
    __relation__ = ''       # specify table name
    
    col_name = db.Column(db.TYPE, primary_key=)
'''


class IngredientCategory(BaseModel, db.Model):

    __tablename__ = 'ingredient_category'

    icid = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    ic_name = db.Column(db.VARCHAR, unique=True)


class Ingredient(BaseModel, db.Model):

    __tablename__ = 'ingredient'

    iid = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    i_name = db.Column(db.VARCHAR, unique=True)
    ic_ids = db.Column(db.ARRAY(db.INTEGER))
    alt_names = db.Column(db.ARRAY(db.TEXT))


class RecipeCategory(BaseModel, db.Model):

    __tablename__ = 'recipe_category'

    rcid = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    rc_name = db.Column(db.VARCHAR, unique=True)


class Step(BaseModel, db.Model):

    __tablename__ = 'step'

    sid = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    s_name = db.Column(db.VARCHAR, unique=True)
    s_detail = db.Column(db.VARCHAR)


class Recipe(BaseModel, db.Model):

    __tablename__ = 'recipe'

    rid = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    r_name = db.Column(db.VARCHAR)
    r_description = db.Column(db.VARCHAR)
    i_id = db.Column(db.INTEGER, ForeignKey('ingredient.iid'))
    rc_id = db.Column(db.INTEGER, ForeignKey('recipe_category.rcid'))
    s_id = db.Column(db.INTEGER, ForeignKey('step.sid'))