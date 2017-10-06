from mealplanner.app import app


@app.route('/')
def index():
    return 'hello flask'