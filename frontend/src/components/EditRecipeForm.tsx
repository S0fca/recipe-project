import { useState } from "react";
import type { Recipe, IngredientInput, Difficulty } from "../types.ts";

interface EditRecipeFormProps {
  recipe: Recipe;
  onRecipeUpdated: () => void;
  onCancel: () => void;
}

export default function EditRecipeForm({ recipe, onRecipeUpdated, onCancel }: EditRecipeFormProps) {
  const [title, setTitle] = useState(recipe.title);
  const [description, setDescription] = useState(recipe.description || "");
  const [difficulty, setDifficulty] = useState<Difficulty>(recipe.difficulty);
  const [isVegetarian, setIsVegetarian] = useState(recipe.is_vegetarian);
  const [ingredients, setIngredients] = useState<IngredientInput[]>(
    recipe.ingredients.map((i) => ({ name: i.name, amount: i.amount, unit: i.unit }))
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleIngredientChange = <K extends keyof IngredientInput>(index: number, field: K, value: IngredientInput[K]) => {
    const newIngredients = [...ingredients];
    newIngredients[index][field] = value;
    setIngredients(newIngredients);
  };

  const addIngredient = () => {
    setIngredients([...ingredients, { name: "", amount: 0, unit: "" }]);
  };

  const removeIngredient = (index: number) => {
    setIngredients(ingredients.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validace: žádný záporný amount
    for (const ing of ingredients) {
      if (ing.amount < 0) {
        setError(`Ingredient '${ing.name}' cannot have negative amount`);
        return;
      }
    }

    setLoading(true);
    setError("");

    try {
      const res = await fetch(`http://127.0.0.1:5000/api/recipes/${recipe.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title,
          description,
          difficulty,
          is_vegetarian: isVegetarian,
          ingredients,
        }),
      });

      const result = await res.json();

      if (!res.ok || !result.success) {
        setError(result.error || "Failed to update recipe");
      } else {
        onRecipeUpdated();
      }
    } catch (err) {
      setError("Failed to update recipe");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="add-form">
      <h2>Edit Recipe</h2>

      <div>
        <label>Title: </label>
        <input value={title} onChange={(e) => setTitle(e.target.value)} required />
      </div>

      <div>
        <label>Description: </label>
        <textarea value={description} onChange={(e) => setDescription(e.target.value)} />
      </div>

      <div>
        <label>Difficulty: </label>
        <select value={difficulty} onChange={(e) => setDifficulty(e.target.value as Difficulty)}>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>

      <div>
        <label>Vegetarian: </label>
        <input type="checkbox" checked={isVegetarian} onChange={(e) => setIsVegetarian(e.target.checked)} />
      </div>

      <h3>Ingredients</h3>
      {ingredients.map((ing, i) => (
        <div key={i} className="ingredient-row">
          <input
            placeholder="Name"
            value={ing.name}
            onChange={(e) => handleIngredientChange(i, "name", e.target.value)}
            required
          />
          <input
            type="number"
            placeholder="Amount"
            value={ing.amount}
            onChange={(e) => handleIngredientChange(i, "amount", parseFloat(e.target.value))}
            required
          />
          <input
            placeholder="Unit"
            value={ing.unit}
            onChange={(e) => handleIngredientChange(i, "unit", e.target.value)}
            required
          />
          <button type="button" onClick={() => removeIngredient(i)}>
            Remove
          </button>
        </div>
      ))}

      <button type="button" onClick={addIngredient}>
        Add Ingredient
      </button>

      <br />
      <button type="submit" disabled={loading}>
        {loading ? "Saving..." : "Save Changes"}
      </button>
      <button type="button" onClick={onCancel} disabled={loading}>
        Cancel
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}
