from mealplanner.__init__ import app


@app.route('/')
def index():
    return 'hello flask'