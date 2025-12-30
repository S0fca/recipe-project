import { useState } from "react";

type ImportResult = {
  imported: number;
  failed: number;
  errors?: { index: number; name?: string; error: string }[];
};

export default function ImportCookbooks() {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setMessage("");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setMessage("Choose JSON file");
      return;
    }

    try {
      const text = await file.text();
      const json = JSON.parse(text);

      const res = await fetch("http://127.0.0.1:5000/api/import/cookbooks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(json),
      });

      const result: ImportResult = await res.json();

      if (!res.ok) {
        setMessage(
          result.errors?.map((e) => `${e.index}: ${e.error}`).join(", ") || "Import failed"
        );
      } else {
        setMessage(`Imported: ${result.imported}, Failed: ${result.failed}`);
      }
    } catch {
      setMessage("Invalid JSON file");
    }
  };

  return (
    <div className="add-form">
      <h3>Import Cookbooks (JSON)</h3>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".json" onChange={handleFileChange} />
        <br />
        <button type="submit">Import Cookbooks</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}
