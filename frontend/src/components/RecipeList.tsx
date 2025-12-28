import { useEffect, useState } from "react";
import type { Recipe } from "../types.ts";

export default function RecipeList() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/recipes")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch recipes");
        return res.json();
      })
      .then((data) => setRecipes(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading recipes...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>Recipes</h2>
      <div className={"recipes-container"}>
        {recipes.map((recipe) => (
        <div key={recipe.id} className="recipe-card">
          <h3>{recipe.title}</h3>
          <p>{recipe.description}</p>
          <p>
            Difficulty: {recipe.difficulty}
          </p>
          <p>
            {recipe.is_vegetarian ? "Vegetarian" : "Non-vegetarian"}
          </p>
          <h4>Ingredients:</h4>
          <ul>
            {recipe.ingredients.map((ing) => (
              <li key={`${recipe.id}-${ing.name}`}>
                {ing.name} - {ing.amount} {ing.unit}
              </li>
            ))}
          </ul>
        </div>
      ))}
      </div>
    </div>
  );
}
