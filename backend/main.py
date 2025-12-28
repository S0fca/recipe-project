from db_init import init_db
from flask import Flask, jsonify, request
from flask_cors import CORS
from recipe_repository import RecipeRepository
from cookbook_repository import CookbookRepository
from model import Ingredient

app = Flask(__name__)
CORS(app)

init_db()

recipe_repo = RecipeRepository()
cookbook_repo = CookbookRepository()




@app.get("/api/recipes")
def get_recipes():
    recipes = recipe_repo.get_all_view()
    return jsonify([r.to_dict() for r in recipes])

@app.post("/api/recipes")
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




@app.post("/api/cookbooks")
def create_cookbook():
    data = request.json
    cookbook = cookbook_repo.create_cookbook(data["name"], data.get("description", ""))
    return jsonify({"id": cookbook.id, "name": cookbook.name, "description": cookbook.description})

@app.get("/api/cookbooks")
def get_cookbooks():
    cookbooks = cookbook_repo.get_all_view()
    return jsonify([c.to_dict() for c in cookbooks])




if __name__ == "__main__":
    app.run(debug=True, port=5000)
