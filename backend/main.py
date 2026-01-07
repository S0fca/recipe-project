from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from db_init import init_db
from service.recipe_service import RecipeService
from service.cookbook_service import (CookbookService)
from service.report_service import ReportService
from model import Ingredient

app = Flask(__name__)
CORS(app)

init_db()

recipe_service = RecipeService()
cookbook_service = CookbookService()
report_service = ReportService()




@app.errorhandler(Exception)
def handle_exception(e):
    code = getattr(e, 'code', 500)
    response = {
        "error": type(e).__name__,
        "description": str(e.description),
        "code": code
    }
    print(f"Error ({code}): {e}")
    return jsonify(response), code





@app.get("/api/recipes")
def get_recipes():
    recipes = recipe_service.get_all_recipes()
    return jsonify([r.to_dict() for r in recipes])

@app.post("/api/recipes")
def add_recipe():
    data = request.json

    if not data or "title" not in data or "ingredients" not in data:
        abort(400, description="Title and ingredients are required")

    ingredients = [
        Ingredient(
            id=None,
            name=i["name"],
            amount=i["amount"],
            unit=i["unit"]
        )
        for i in data["ingredients"]
    ]

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
        abort(400, description="Invalid import format")

    result = recipe_service.import_recipes(data["recipes"])
    return jsonify(result), 200

@app.delete("/api/recipes/<int:recipe_id>")
def delete_recipe(recipe_id: int):
    result = recipe_service.delete_recipe(recipe_id)

    if not result["success"]:
        abort(404, description=result.get("error", "Recipe not found"))

    return jsonify({"message": result["message"]}), 200

@app.put("/api/recipes/<int:recipe_id>")
def update_recipe(recipe_id: int):
    data = request.json

    if not data or "title" not in data or "ingredients" not in data:
        abort(400, description="Title and ingredients are required")

    ingredients = [
        Ingredient(
            id=None,
            name=i["name"],
            amount=i["amount"],
            unit=i["unit"]
        )
        for i in data["ingredients"]
    ]

    result = recipe_service.edit_recipe(
        recipe_id,
        title=data["title"],
        description=data.get("description", ""),
        difficulty=data.get("difficulty", "easy"),
        is_vegetarian=data.get("is_vegetarian", False),
        ingredients=ingredients
    )

    if not result.get("success"):
        abort(400, description=result.get("error", "Failed to update recipe"))

    return jsonify(result), 200




@app.get("/api/cookbooks")
def get_cookbooks():
    cookbooks = cookbook_service.get_all_cookbooks()
    return jsonify([c.to_dict() for c in cookbooks])

@app.post("/api/cookbooks")
def create_cookbook():
    data = request.json

    if not data or "name" not in data:
        abort(400, description="Name is required")

    cookbook = cookbook_service.create_cookbook(
        data["name"],
        data.get("description", "")
    )

    return jsonify({
        "id": cookbook.id,
        "name": cookbook.name,
        "description": cookbook.description
    }), 201

@app.post("/api/cookbooks/<int:cookbook_id>/recipes/<int:recipe_id>")
def add_recipe_to_cookbook(cookbook_id: int, recipe_id: int):
    result = cookbook_service.add_recipe_to_cookbook(cookbook_id, recipe_id)

    if not result["success"]:
        abort(400, description=result.get("error", "Failed to add recipe to cookbook"))

    return jsonify(result), 200

@app.get("/api/cookbooks/<int:cookbook_id>/recipes")
def get_cookbook_recipes(cookbook_id: int):
    recipes = cookbook_service.get_cookbook_recipes(cookbook_id)
    return jsonify([r.to_dict() for r in recipes])

@app.post("/api/import/cookbooks")
def import_cookbooks():
    data = request.json

    if not data or "cookbooks" not in data:
        abort(400, description="Invalid import format")

    result = cookbook_service.import_cookbooks(data["cookbooks"])
    return jsonify(result), 200

@app.delete("/api/cookbooks/<int:cookbook_id>")
def delete_cookbook(cookbook_id: int):
    result = cookbook_service.delete_cookbook(cookbook_id)

    if not result["success"]:
        abort(404, description=result.get("error", "Cookbook not found"))

    return jsonify({"message": result["message"]}), 200


@app.get("/api/report/summary")
def get_summary_report():
    report = report_service.get_summary()
    return jsonify(report), 200




if __name__ == "__main__":
    app.run(debug=True, port=5000)
