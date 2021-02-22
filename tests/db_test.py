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

def test_create_models(db_handle):
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
    ingrtest = Ingredient.query.all()[2]
    assert first_iim.meal == Meal.query.first()
    # kirjoittele tähän lisää kunhan jaksat

    

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
