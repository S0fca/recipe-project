import './App.css'
import RecipeList from "./components/RecipeList.tsx";
import AddRecipeForm from "./components/AddRecipeForm.tsx";
import CookbookList from "./components/CookbookList.tsx";
import AddCookbookForm from "./components/AddCookbookForm.tsx";
import {useState} from "react";
import ImportRecipes from "./components/ImportRecipes.tsx";
import AddRecipeToCookbook from "./components/AddRecipeToCookbook.tsx";
import ImportCookbooks from "./components/ImportCookbooks.tsx";
import SummaryReport from "./components/SummaryReport.tsx";

function App() {
  const [activeTab, setActiveTab] = useState<"recipes" | "cookbooks" | "report">("recipes");

  return (
      <>
          <h1>
              Recipe app
          </h1>

          <div style={{marginBottom: "20px"}}>
              <button style={{margin: "10px"}} onClick={() => setActiveTab("recipes")}>Recipes</button>
              <button style={{margin: "10px"}} onClick={() => setActiveTab("cookbooks")}>Cookbooks</button>
              <button style={{margin: "10px"}} onClick={() => setActiveTab("report")}>Report</button>
          </div>

          {activeTab === "recipes" && (
              <>
                  <RecipeList/>
                  <AddRecipeForm onRecipeAdded={() => window.location.reload()}/>
                <ImportRecipes />
            </>
          )}

          {activeTab === "cookbooks" && (
            <>
                <CookbookList/>
                <AddCookbookForm onCookbookAdded={() => window.location.reload()}/>
                <AddRecipeToCookbook />
                <ImportCookbooks />
            </>
          )}

          {activeTab === "report" && (
            <>
                <SummaryReport />
            </>
          )}
      </>
  )
}

export default App
