from db_init import init_db
from flask import Flask, jsonify, request
from flask_cors import CORS
from recipe_repository import RecipeRepository
from model import Ingredient

app = Flask(__name__)
CORS(app)

init_db()

recipe_repo = RecipeRepository()

@app.route("/api/recipes", methods=["GET"])
def get_recipes():
    recipes = recipe_repo.get_all_view()
    return jsonify([r.to_dict() for r in recipes])

@app.route("/api/recipes", methods=["POST"])
def add_recipe():
    data = request.json
    if not data or "title" not in data or "ingredients" not in data:
        return jsonify({"error": "Title and ingredients are required"}), 400

    ingredients = []
    for ing in data["ingredients"]:
        ingredients.append(Ingredient(
            id=None,
            name=ing.get("name"),
            amount=ing.get("amount"),
            unit=ing.get("unit")
        ))

    try:
        recipe = recipe_repo.add_recipe_with_ingredients(
            title=data["title"],
            description=data.get("description", ""),
            difficulty=data.get("difficulty", "easy"),
            is_vegetarian=data.get("is_vegetarian", False),
            ingredients=ingredients
        )
        return jsonify(recipe), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
