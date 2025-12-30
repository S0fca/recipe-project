from db_init import init_db
from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.service.recipe_service import RecipeService
from backend.service.cookbook_service import CookbookService
from backend.service.report_service import ReportService
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

@app.delete("/api/recipes/<int:recipe_id>")
def delete_recipe(recipe_id: int):
    result = recipe_service.delete_recipe(recipe_id)
    if result["success"]:
        return jsonify({"message": result["message"]}), 200
    else:
        return jsonify({"error": result["error"]}), 404

@app.put("/api/recipes/<int:recipe_id>")
def update_recipe(recipe_id: int):
    data = request.json
    if not data or "title" not in data or "ingredients" not in data:
        return jsonify({"success": False, "error": "Title and ingredients are required"}), 400

    ingredients = [
        Ingredient(id=None, name=i["name"], amount=i["amount"], unit=i["unit"])
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

    status_code = 200 if result.get("success") else 400
    return jsonify(result), status_code



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

@app.post("/api/cookbooks/<int:cookbook_id>/recipes/<int:recipe_id>")
def add_recipe_to_cookbook(cookbook_id: int, recipe_id: int):
    result = cookbook_service.add_recipe_to_cookbook(cookbook_id, recipe_id)
    status = 200 if result["success"] else 400
    return jsonify(result), status

@app.get("/api/cookbooks/<int:cookbook_id>/recipes")
def get_cookbook_recipes(cookbook_id: int):
    try:
        recipes = cookbook_service.get_cookbook_recipes(cookbook_id)
        return jsonify([r.to_dict() for r in recipes])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post("/api/import/cookbooks")
def import_cookbooks():
    data = request.json
    if not data or "cookbooks" not in data:
        return jsonify({"error": "Invalid import format"}), 400

    try:
        result = cookbook_service.import_cookbooks(data["cookbooks"])
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





@app.get("/api/report/summary")
def get_summary_report():
    try:
        report = report_service.get_summary()
        return jsonify(report), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True, port=5000)
