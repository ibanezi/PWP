from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False, unique=True)

    meals = db.relationship("Meal", back_populates="user")

class Meal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userId = db.Column(db.Integer, db.ForeignKey("user.id"))
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(255))

	user = db.relationship("User", back_populates="meals")
	ingredients = db.relationship("IngredientsInMeal", back_populates="meal")

class Ingredient(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	ssize = db.Column(db.Float, nullable=False)
	kcal = db.Column(db.Float, nullable=False)
	carbs = db.Column(db.Float)
	proteins = db.Column(db.Float)
	fats = db.Column(db.Float)

	meal = db.relationship("IngredientsInMeal", back_populates="ingredients")

class IngredientsInMeal(db.Model):
	mealId = db.Column(db.Integer, db.ForeignKey("meal.id"), primary_key=True)
	ingredientId = db.Column(db.Integer, db.ForeignKey("ingredients.id"), primary_key=True)
	ssize = db.Column(db.Float, nullable=False)

	meal = db.relationship("Meal", back_populates="ingredients")
	ingredients = db.relationship("Ingredient", back_populates="meal")

