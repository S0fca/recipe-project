import { useState } from "react";
import type { Difficulty, IngredientInput } from "../types.ts";

interface AddRecipeFormProps {
  onRecipeAdded: () => void;
}

export default function AddRecipeForm({ onRecipeAdded }: AddRecipeFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [difficulty, setDifficulty] = useState<"easy" | "medium" | "hard">("easy");
  const [isVegetarian, setIsVegetarian] = useState(false);
  const [ingredients, setIngredients] = useState<IngredientInput[]>([
    { name: "", amount: 0, unit: "" },
  ]);

  const handleIngredientChange = <K extends keyof IngredientInput>(
  index: number,
  field: K,
  value: IngredientInput[K]
) => {
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

    try {
      const res = await fetch("http://127.0.0.1:5000/api/recipes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title,
          description,
          difficulty,
          is_vegetarian: isVegetarian,
          ingredients,
        }),
      });

      if (!res.ok) throw new Error("Failed to add recipe");

      setTitle("");
      setDescription("");
      setDifficulty("easy");
      setIsVegetarian(false);
      setIngredients([{ name: "", amount: 0, unit: "" }]);

      onRecipeAdded();
    } catch (err) {
      console.error(err);
      alert("Error adding recipe");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="add-form">
      <h2>Add Recipe</h2>

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

      <div className={"ingredient-row"}>
        <label>Vegetarian: </label>
        <input
          type="checkbox"
          checked={isVegetarian}
          onChange={(e) => setIsVegetarian(e.target.checked)}
        />
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
      <button type="submit">Add Recipe</button>
    </form>
  );
}
