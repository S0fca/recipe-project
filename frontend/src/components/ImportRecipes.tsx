import { useState } from "react";
import type { ChangeEvent, FormEvent } from "react";

export default function ImportRecipes() {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string>("");

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setMessage("");
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!file) {
      setMessage("Choose JSON file");
      return;
    }

    try {
      const text = await file.text();
      const json = JSON.parse(text);

      const res = await fetch("http://127.0.0.1:5000/api/import/recipes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(json),
      });

      const data = await res.json();

      if (!res.ok) {
        setMessage(data.description || "Import failed");
      } else {
        const errorsDesc = " " + data.errors
          .map((e: { error: string }) => e.error)
          .join(", ");

        setMessage(
          `Import done: ${data.imported} OK, ${data.failed} errors ${errorsDesc}`
        );
      }
    } catch (err) {
      console.log(err)
      setMessage("Invalid JSON file");
    }
  };

  return (
    <div className="add-form">
      <h3>Import recipes (JSON)</h3>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".json" onChange={handleFileChange} />
        <br />
        <button type="submit">Import recipes</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}
