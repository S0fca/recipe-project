import { useEffect, useState } from "react";
import type { Recipe } from "../types.ts";
import EditRecipeForm from "./EditRecipeForm.tsx";

export default function RecipeList() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState<Recipe | null>(null);

  const fetchRecipes = async () => {
    setLoading(true);
    setError(null);
    fetch("http://127.0.0.1:5000/api/recipes")
      .then(res => {
        if (!res.ok) {
            throw new Error("Failed to load recipes");
        }
        return res.json();
      })
      .then(data => setRecipes(data))
      .catch(() => setError("Failed to load recipes"))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchRecipes();
  }, []);

  const handleDelete = async (id: number) => {
    try {
      const res = await fetch(`http://127.0.0.1:5000/api/recipes/${id}`, {
        method: "DELETE",
      });
      const result = await res.json();

      if (!res.ok) throw new Error(result.error || "Failed to delete recipe");

      setRecipes((prev) => prev.filter((r) => r.id !== id));
    } catch (err: any) {
      alert(`Error deleting recipe: ${err.message}`);
    }
  };

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
            <p>Difficulty: {recipe.difficulty}</p>
            <p>{recipe.is_vegetarian ? "Vegetarian" : "Non-vegetarian"}</p>
            <h4>Ingredients:</h4>
            <ul>
              {recipe.ingredients.map((ing) => (
                <li key={`${recipe.id}-${ing.name}`}>
                  {ing.name} - {ing.amount} {ing.unit}
                </li>
              ))}
            </ul>
            <button style={{margin: "10px"}} onClick={() => handleDelete(recipe.id)}>Delete</button>
            <button style={{margin: "10px"}} onClick={() => setEditing(recipe)}>Edit</button>
          </div>
        ))}
      </div>

      {editing && (
        <EditRecipeForm
          recipe={editing}
          onRecipeUpdated={() => {
            setEditing(null);
            fetchRecipes();
          }}
          onCancel={() => setEditing(null)}
        />
      )}
    </div>
  );
}
