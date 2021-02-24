from os import path, remove
from sqlalchemy import event
from sqlalchemy.engine import Engine
from CalorieTracker.models import *

# Set foreign keys support
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

DB_PATH = path.join('.', 'CalorieTracker', 'test.db')

# Delete database because we are populating with values that have uniqueness constraint (user.name)
if path.isfile(DB_PATH):
    print('Old testing database exists, deleting...')
    remove(DB_PATH)

db.create_all()

# Populate database with test data
users = [User(name='TestUser1'), User(name='TestUser2'), User(name='TestUser3'), User(name='TestUser4')]
for u in users:
    db.session.add(u)
db.session.commit()

ingreds = [Ingredient(
        name='Tomato',
        ssize=100,
        kcal=23,
        carbs=62,
        proteins=10,
        fats=12
        ),
    Ingredient(
        name='Potato',
        ssize=150,
        kcal=112,
        carbs=125,
        proteins=15,
        fats=2
        ),
    Ingredient(
        name='Beer',
        ssize=330,
        kcal=142,
        carbs=128,
        proteins=13,
        fats=0
        ),
    Ingredient(
        name='Ground beef',
        ssize=400,
        kcal=648,
        carbs=0,
        proteins=208,
        fats=192
        ),
    Ingredient(
        name='Egg',
        ssize=60,
        kcal=80,
        carbs=0,
        proteins=23,
        fats=36
        ),
    Ingredient(
        name='Lazy potato',
        ssize=150,
        kcal=110
        )]

for i in ingreds:
    db.session.add(i)
db.session.commit()

meals = [
    Meal(
        userId=3,
        name='Breakfast',
        description='Sunday morning breakfast'
        ),
    Meal(
        userId=1,
        name='Dinner'
        ),
    Meal(
        userId=2,
        name='Breakfast',
        description='Omelette with tomatoes'
        )
    ]

for m in meals:
    db.session.add(m)
db.session.commit()

meal_items = [
    IngredientsInMeal(
        mealId=1,
        ingredientId=3,
        ssize=6
        ),
    IngredientsInMeal(
        mealId=2,
        ingredientId=2,
        ssize=3
        ),
    IngredientsInMeal(
        mealId=2,
        ingredientId=4,
        ssize=0.3
        ),
    IngredientsInMeal(
        mealId=3,
        ingredientId=5,
        ssize=2
        ),
    IngredientsInMeal(
        mealId=3,
        ingredientId=1,
        ssize=3
        )
    ]

for mi in meal_items:
    db.session.add(mi)
db.session.commit()
