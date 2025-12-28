from typing import List, Optional

class Ingredient:
    def __init__(self, id: int, name: str, amount: float = None, unit: str = None):
        self.id = id
        self.name = name
        self.amount = amount
        self.unit = unit

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "unit": self.unit
        }


class Recipe:
    def __init__(self, id: int, title: str, description: str, difficulty: str,
                 is_vegetarian: bool, created_at=None, ingredients: List[Ingredient] = None):
        self.id = id
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.is_vegetarian = is_vegetarian
        self.created_at = created_at
        self.ingredients = ingredients or []

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "difficulty": self.difficulty,
            "is_vegetarian": self.is_vegetarian,
            "created_at": str(self.created_at),
            "ingredients": [ing.to_dict() for ing in self.ingredients]
        }

class Cookbook:
    def __init__(self, id: int, name: str, description: str, recipe_count: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.recipe_count = recipe_count

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "recipe_count": self.recipe_count
        }
