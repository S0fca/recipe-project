import { useState } from "react";

interface AddCookbookFormProps {
  onCookbookAdded: () => void;
}

export default function AddCookbookForm({ onCookbookAdded }: AddCookbookFormProps) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:5000/api/cookbooks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description }),
      });

      if (!res.ok) throw new Error("Failed to add cookbook");

      setName("");
      setDescription("");
      onCookbookAdded();
    } catch (err) {
      console.error(err);
      alert("Error adding cookbook");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="add-form">
      <h2>Add Cookbook</h2>
      <div>
        <label>Name:</label>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Description:</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>
      <button type="submit" disabled={loading}>
        {loading ? "Adding..." : "Add Cookbook"}
      </button>
    </form>
  );
}
