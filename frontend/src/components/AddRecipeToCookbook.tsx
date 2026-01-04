import { useEffect, useState } from "react";
import type { Recipe, Cookbook } from "../types.ts";

type Props = {
  onAdded?: () => void;
};

export default function AddRecipeToCookbook({ onAdded }: Props) {

  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [cookbooks, setCookbooks] = useState<Cookbook[]>([]);
  const [selectedRecipe, setSelectedRecipe] = useState<number | "">("");
  const [selectedCookbook, setSelectedCookbook] = useState<number | "">("");
  const [message, setMessage] = useState<string>("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/recipes")
      .then((res) => res.json())
      .then((data) => setRecipes(data))
      .catch((err) => console.error("Error loading recipes:", err));

    fetch("http://127.0.0.1:5000/api/cookbooks")
      .then((res) => res.json())
      .then((data) => setCookbooks(data))
      .catch((err) => console.error("Error loading cookbooks:", err));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");

    if (selectedRecipe === "" || selectedCookbook === "") {
      setMessage("Please select both a recipe and a cookbook.");
      return;
    }

    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/cookbooks/${selectedCookbook}/recipes/${selectedRecipe}`,
        { method: "POST" }
      );
      const result = await res.json();

      if (!res.ok) {
        setMessage(result.error || "Failed to add recipe to cookbook.");
      } else {
        setMessage(result.message || "Recipe added successfully!");
        onAdded?.();
      }
    } catch (err: any) {
      setMessage("Error: " + err.message);
    }
  };

  return (
    <div className="add-form">
      <h3>Add Recipe to Cookbook</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Recipe:</label>
          <select
            value={selectedRecipe}
            onChange={(e) => setSelectedRecipe(Number(e.target.value))}
          >
            <option value="">Select recipe</option>
            {recipes.map((r) => (
              <option key={r.id} value={r.id}>
                {r.title}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label>Cookbook:</label>
          <select
            value={selectedCookbook}
            onChange={(e) => setSelectedCookbook(Number(e.target.value))}
          >
            <option value="">Select cookbook</option>
            {cookbooks.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>

        <button type="submit">Add Recipe</button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}
