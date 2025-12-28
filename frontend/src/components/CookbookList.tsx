import { useEffect, useState } from "react";
import type { Cookbook } from "../types";

export default function CookbookList() {
  const [cookbooks, setCookbooks] = useState<Cookbook[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/cookbooks")
      .then(res => {
        if (!res.ok) throw new Error("Failed to fetch cookbooks");
        return res.json();
      })
      .then(data => setCookbooks(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading cookbooks...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
      <>
          <h2>Cookbooks</h2>
          <div className="recipes-container">
              {cookbooks.length === 0 && <p>No cookbooks yet.</p>}
              {cookbooks.map(cb => (
                  <div key={cb.id} className="recipe-card">
                      <h3>{cb.name}</h3>
                      <p>{cb.description}</p>
                      <p>Recipes: {cb.recipe_count}</p>
                  </div>
              ))}
          </div>
      </>
  );
}
