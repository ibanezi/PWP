import json
from flask import request, Response, url_for
from flask_restful import Resource

class IngredientItem(resource):
    def get():
        # Get ingredient information
        pass

    def put():
        # Edit ingredient information
        pass

    def delete():
        # Delete ingredient
        pass

class IngredientCollection(resource):
    def get():
        # Get list of all ingredients
        pass

    def post():
        # Add an ingredient
        pass
