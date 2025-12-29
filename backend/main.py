from db_init import init_db
from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.service.recipe_service import RecipeService
from backend.service.cookbook_service import CookbookService
from model import Ingredient

app = Flask(__name__)
CORS(app)

init_db()

recipe_service = RecipeService()
cookbook_service = CookbookService()




@app.errorhandler(Exception)
def handle_exception(e):
    code = getattr(e, 'code', 500)
    response = {
        "error": type(e).__name__,
        "description": str(e),
        "code": code
    }
    print(f"Error ({code}): {e}")
    return jsonify(response), code





@app.get("/api/recipes")
def get_recipes():
    try:
        recipes = recipe_service.get_all_recipes()
        return jsonify([r.to_dict() for r in recipes])
    except Exception as e:
        raise e

@app.post("/api/recipes")
def add_recipe():
    data = request.json
    if not data or "title" not in data or "ingredients" not in data:
        return jsonify({"error": "Bad Request", "description": "Title and ingredients are required"}), 400

    ingredients = [Ingredient(id=None, name=i["name"], amount=i["amount"], unit=i["unit"])
                   for i in data["ingredients"]]

    recipe = recipe_service.add_recipe(
        title=data["title"],
        description=data.get("description", ""),
        difficulty=data.get("difficulty", "easy"),
        is_vegetarian=data.get("is_vegetarian", False),
        ingredients=ingredients
    )
    return jsonify(recipe), 201

@app.post("/api/import/recipes")
def import_recipes():
    data = request.json
    if not data or "recipes" not in data:
        return jsonify({"error": "Bad Request", "description": "Invalid import format"}), 400

    result = recipe_service.import_recipes(data["recipes"])
    return jsonify(result), 200





@app.get("/api/cookbooks")
def get_cookbooks():
    cookbooks = cookbook_service.get_all_cookbooks()
    return jsonify([c.to_dict() for c in cookbooks])

@app.post("/api/cookbooks")
def create_cookbook():
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Bad Request", "description": "Name is required"}), 400

    cookbook = cookbook_service.create_cookbook(data["name"], data.get("description", ""))
    return jsonify({"id": cookbook.id, "name": cookbook.name, "description": cookbook.description}), 201








if __name__ == "__main__":
    app.run(debug=True, port=5000)
