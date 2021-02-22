import os, sys
import pytest
import tempfile
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from CalorieTracker.models import *


# Set foreign keys support
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Create temporary empty database
@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.config["TESTING"] = True
    
    db.create_all()
        
    yield db
    
    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)



def _get_user(num='1'):
    return User(
        name='Username'+num
    )

def _get_meal(num='1', uid=1):
    return Meal(
        userId=uid,
        name='Meal'+num,
        description='Description'
    )

def _get_ingredient(num='1'):
    return Ingredient(
        name='Ingredient'+num,
        ssize=100.12,
        kcal=200,
        carbs=50.7,
        proteins=20.4,
        fats=12.1
    )

# Test creation of instance for each model
def test_models_create(db_handle):
    user1 = _get_user()
    user2 = _get_user(num='2')
    meal1 = _get_meal()
    
    meal2 = _get_meal(num='2')
    
    ingr1 = _get_ingredient()
    ingr2 = _get_ingredient(num='2')
    ingr3 = _get_ingredient(num='3')

    db_handle.session.add(user1)
    db_handle.session.commit()
    assert User.query.count() == 1
    db_handle.session.add(user2)
    db_handle.session.commit()
    assert User.query.count() == 2
    meal1.user = user1
    db_handle.session.add(meal1)
    db_handle.session.commit()
    assert Meal.query.count() == 1
    meal2.user = user2
    db_handle.session.add(meal2)
    db_handle.session.commit()
    assert Meal.query.count() == 2
    db_handle.session.add(ingr1)
    db_handle.session.commit()
    assert Ingredient.query.count() == 1
    db_handle.session.add(ingr2)
    db_handle.session.add(ingr3)
    db_handle.session.commit()
    assert Ingredient.query.count() == 3

    ingr_in_meal = IngredientsInMeal(
        mealId=meal1.id,
        ingredientId=ingr3.id,
        ssize=1.5
        )
    db_handle.session.add(ingr_in_meal)
    db_handle.session.commit()
    assert IngredientsInMeal.query.count() == 1
    first_iim = IngredientsInMeal.query.first()
    assert first_iim.meal == Meal.query.first()
    # kirjoittele tähän lisää kunhan jaksat

def test_user_query(db_handle):
    user1 = _get_user()
    user2 = _get_user(num='2')
    user2.name = 'I am second'

    db_handle.session.add(user1)
    db_handle.session.add(user2)
    db_handle.session.commit()

    assert user1.id == User.query.filter_by(name='Username1').first().id
    assert user2.id == User.query.filter_by(name='I am second').first().id


def test_user_modify(db_handle):
    user1 = _get_user()
    user2 = _get_user(num='2')

    db_handle.session.add(user1)
    db_handle.session.add(user2)
    db_handle.session.commit()
    before = [user1.name, user2.name]
    user1.name = 'NewUserName'
    db_handle.session.commit()

    after = [User.query.get(1).name, User.query.get(2).name]
    assert before[0] != after[0]
    assert before[1] == after[1]
    
def test_user_delete(db_handle):
    user1 = _get_user()
    user2 = _get_user(num='2')

    db_handle.session.add(user1)
    db_handle.session.add(user2)
    db_handle.session.commit()
    assert User.query.count() == 2
    db_handle.session.delete(user1)
    db_handle.session.commit()
    assert User.query.count() == 1
    assert user2.id == 2

def test_unique_constraint(db_handle):
    user1 = _get_user('uniq')
    user2 = _get_user('uniquu')
    db_handle.session.add(user1)
    db_handle.session.add(user2)
    db_handle.session.commit(
        )
    user3 = _get_user('uniq')
    db_handle.session.add(user3)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
        
def test_ingredient_query(db_handle):
    ingredient1 = _get_ingredient()
    ingredient2 = _get_ingredient(num='2')
    ingredient2.name = 'I am second'

    db_handle.session.add(ingredient1)
    db_handle.session.add(ingredient2)
    db_handle.session.commit()

    assert (ingredient1.id == Ingredient.query.filter_by(name='Ingredient1').first().id)
    assert (ingredient2.id == Ingredient.query.filter_by(name='I am second').first().id)

def test_ingredient_modify(db_handle):
    ingredient1 = _get_ingredient()

    db_handle.session.add(ingredient1)
    db_handle.session.commit()
    assert (1 == Ingredient.query.count())

    db_ingredient = Ingredient.query.first()
    assert (200 == db_ingredient.kcal)

    ingredient1.kcal = 350
    db_handle.session.commit()
    db_ingredient = Ingredient.query.first()
    assert (350 == db_ingredient.kcal)

def test_ingredient_delete(db_handle):
    ingredient1 = _get_ingredient()
    ingredient2 = _get_ingredient(num='2')

    db_handle.session.add(ingredient1)
    db_handle.session.add(ingredient2)
    db_handle.session.commit()
    assert (2 == Ingredient.query.count())

    db_handle.session.delete(ingredient1)
    db_handle.session.commit()
    assert (1 == Ingredient.query.count())

def test_meal_query(db_handle):
    user = _get_user()
    meal1 = _get_meal()
    meal2 = _get_meal(num='2')
    meal2.name = 'I am second'

    db_handle.session.add(user)
    db_handle.session.add(meal1)
    db_handle.session.add(meal2)
    db_handle.session.commit()

    assert (meal1.id == Meal.query.filter_by(name='Meal1').first().id)
    assert (meal2.id == Meal.query.filter_by(name='I am second').first().id)

def test_meal_modify(db_handle):
    user = _get_user()
    meal = _get_meal()

    db_handle.session.add(user)
    db_handle.session.add(meal)
    db_handle.session.commit()
    assert User.query.count() == 1
    assert Meal.query.count() == 1

    db_meal = Meal.query.first()
    assert ('Meal1' == db_meal.name)

    meal.name = 'Kurkkusalaatti'
    db_handle.session.commit()
    db_meal = Meal.query.first()
    assert ('Kurkkusalaatti' == db_meal.name)

def test_meal_delete(db_handle):
    user = _get_user()
    meal1 = _get_meal()
    meal2 = _get_meal(num='2')

    db_handle.session.add(user)
    db_handle.session.add(meal1)
    db_handle.session.add(meal2)
    db_handle.session.commit
    assert (2 == Meal.query.count())

    db_handle.session.delete(meal1)
    db_handle.session.commit()
    assert (1 == Meal.query.count())
        
