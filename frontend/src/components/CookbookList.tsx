import { useEffect, useState } from "react";
import type { Cookbook } from "../types";
import CookbookDetails from "./CookbookDetails.tsx";

export default function CookbookList() {
  const [cookbooks, setCookbooks] = useState<Cookbook[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCookbook, setSelectedCookbook] = useState<Cookbook | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/cookbooks")
      .then(res => {
        if (!res.ok) {
            throw new Error("Failed to load cookbooks");
        }
        return res.json();
      })
      .then(data => setCookbooks(data))
      .catch(() => setError("Failed to load cookbooks"))
      .finally(() => setLoading(false));
  }, []);

  const handleDelete = async (id: number) => {
        try {
          const res = await fetch(`http://127.0.0.1:5000/api/cookbooks/${id}`, {
            method: "DELETE",
          });
          const result = await res.json();

          if (!res.ok) throw new Error(result.error || "Failed to delete cookbook");

          setCookbooks((prev) => prev.filter((c) => c.id !== id));
        } catch (err: any) {
          alert(`Error deleting recipe: ${err.message}`);
        }
  }

  if (loading) return <p>Loading cookbooks...</p>;
  if (error) return <p>Error: {error}</p>;

    return (
      <>
          <h2>Cookbooks</h2>
          <div className="recipes-container">
              {cookbooks.length === 0 && <p>No cookbooks yet.</p>}
              {cookbooks.map(cb => (
                  <span onClick={() => setSelectedCookbook(cb)}
                        style={{cursor: "pointer"}}>
                      <div key={cb.id} className="recipe-card">
                          <h3>{cb.name}</h3>
                          <p>{cb.description}</p>
                          <p>Recipes: {cb.recipe_count}</p>
                          <button style={{margin: "10px"}}
                                              onClick={() => handleDelete(cb.id)}>Delete</button>

                      </div>
                  </span>
              ))}
          </div>
          {selectedCookbook && (
              <CookbookDetails cookbook={selectedCookbook} onClose={() => setSelectedCookbook(null)} />
          )}
      </>
  );
}
