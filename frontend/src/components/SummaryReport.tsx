import { useEffect, useState } from "react";

export default function SummaryReport() {
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/report/summary")
      .then(res => {
        if (!res.ok) throw new Error("Failed to fetch report");
        return res.json();
      })
      .then(data => setReport(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading report...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!report) return null;

  return (
    <div className="report">
      <h2>Summary Report</h2>
      <ul>
        <li>Total Recipes: {report.total_recipes}</li>
        <li>Total Cookbooks: {report.total_cookbooks}</li>
        <li>Total Ingredients: {report.total_ingredients}</li>
        <li>Avg Ingredients per Recipe: {report.avg_ingredients_per_recipe.toFixed(2)}</li>
        <li>Min Ingredients in a Recipe: {report.min_ingredients_in_recipe}</li>
        <li>Max Ingredients in a Recipe: {report.max_ingredients_in_recipe}</li>
        <li>Avg Recipes per Cookbook: {report.avg_recipes_per_cookbook.toFixed(2)}</li>
        <li>Min Recipes in a Cookbook: {report.min_recipes_in_cookbook}</li>
        <li>Max Recipes in a Cookbook: {report.max_recipes_in_cookbook}</li>
      </ul>
    </div>
  );
}
