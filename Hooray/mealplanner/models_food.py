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


class Recipes(BaseModel, db.Model):

    __relation__ = 'recipes'

    rid = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    r_name = db.Column(db.VARCHAR)
    r_description = db.Column(db.VARCHAR)

    def __repr__(self):
        return '<Recipe [%r] %r >' % (self.id, self.name)


class Ingredients(BaseModel, db.Model):

    __relation__ = 'ingredients'

    iid = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    i_name = db.Column(db.VARCHAR)
    i_description = db.Column(db.VARCHAR)
    r_id = db.Column(db.INTEGER, ForeignKey('recipes.rid'))

    def __repr__(self):
        return '<Ingredient [%r] %r>' % (self.iid, self.i_name)


class Steps(BaseModel, db.Model):

    __relation__ = 'steps'

    sid = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    s_name = db.Column(db.VARCHAR)
    s_detail = db.Column(db.VARCHAR)
    r_id = db.Column(db.INTEGER, ForeignKey('recipes.rid'))

    def __repr__(self):
        return '<Step [%r] %r>' % (self.sid, self.s_detail)


class IngredientCategory(BaseModel, db.Model):

    __relation__ = 'ingredients_categories'

    cid = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    c_name = db.Column(db.VARCHAR)
    i_id = db.Column(db.INTEGER, ForeignKey('ingredients.iid'))