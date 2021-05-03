from flask_restful import Api
from CalorieTracker.resources.user import UserItem, UserCollection
from CalorieTracker.resources.meal import MealItem, MealCollection
from CalorieTracker.resources.ingredient import IngredientItem, IngredientCollection

api = Api()
api.app_resource(UserItem, '/api/users/<user>/')
api.app_resource(UserCollection, '/api/users/')
api.app_resource(MealItem, '/api/users/<user>/meals/<meal>/')
api.app_resource(MealCollection, '/api/users/<user>/meals/')
api.app_resource(IngredientItem, '/api/ingredients/<ingredient>')
api.app_resource(IngredientCollection, '/api/ingredients/')
