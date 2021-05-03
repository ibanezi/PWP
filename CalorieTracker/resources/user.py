import json
from flask import request, Response, url_for
from flask_restful import Resource

class UserItem(resource):
    def get():
        # Get user information
        pass

    def put():
        # Edit user information
        pass

    def delete():
        # Delete user
        pass

class UserCollection(resource):
    def get():
        # Get list of all users
        pass

    def post():
        # Add a new user
        pass
