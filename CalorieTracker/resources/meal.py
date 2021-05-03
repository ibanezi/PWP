import json
from flask import request, Response, url_for
from flask_restful import Resource

class MealItem(resource):
    def get():
        # Get meal information
        pass

    def put():
        # Edit meal information
        pass

    def post():
        # Add ingredient to meal
        pass

    def delete():
        # Delete meal
        pass

class MealCollection(resource):
    def get():
        # Get list of user's meals
        pass

    def post():
        # Add a meal
        pass