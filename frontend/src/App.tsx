import './App.css'
import RecipeList from "./components/RecipeList.tsx";
import AddRecipeForm from "./components/AddRecipeForm.tsx";
import CookbookList from "./components/CookbookList.tsx";
import AddCookbookForm from "./components/AddCookbookForm.tsx";
import {useState} from "react";

function App() {
  const [activeTab, setActiveTab] = useState<"recipes" | "cookbooks">("recipes");

  return (
      <>
          <h1>
              Recipe app
          </h1>

          <div style={{marginBottom: "20px"}}>
              <button style={{margin: "10px"}} onClick={() => setActiveTab("recipes")}>Recepty</button>
              <button style={{margin: "10px"}} onClick={() => setActiveTab("cookbooks")}>Kuchařky</button>
          </div>

          {activeTab === "recipes" && (
            <>
                <RecipeList/>
                <AddRecipeForm onRecipeAdded={() => window.location.reload()}/>
            </>
          )}

          {activeTab === "cookbooks" && (
            <>
              <CookbookList/>
              <AddCookbookForm onCookbookAdded={() => window.location.reload()}/>
            </>
          )}
      </>
  )
}

export default App
