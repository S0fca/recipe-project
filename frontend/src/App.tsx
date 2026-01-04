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
    const [activeTab, setActiveTab] = useState<"recipes" | "cookbooks" | "report">(
        () => (localStorage.getItem("activeTab") as any) || "recipes"
    );

    const changeTab = (tab: "recipes" | "cookbooks" | "report") => {
        setActiveTab(tab);
        localStorage.setItem("activeTab", tab);
    };

    const [refreshKey, setRefreshKey] = useState(0);
    const refresh = () => setRefreshKey(k => k + 1);

  return (
      <>
          <h1>
              Recipe app
          </h1>

          <div style={{marginBottom: "20px"}}>
              <button style={{margin: "10px"}} onClick={() => changeTab("recipes")}>Recipes</button>
              <button style={{margin: "10px"}} onClick={() => changeTab("cookbooks")}>Cookbooks</button>
              <button style={{margin: "10px"}} onClick={() => changeTab("report")}>Report</button>
          </div>

          {activeTab === "recipes" && (
              <>
                  {activeTab === "recipes" && (
                      <>
                        <RecipeList key={refreshKey} />
                        <AddRecipeForm onRecipeAdded={refresh} />
                        <ImportRecipes onImported={refresh} />
                      </>
                  )}
              </>
          )}

          {activeTab === "cookbooks" && (
            <>
              <CookbookList key={refreshKey} />
              <AddCookbookForm onCookbookAdded={refresh} />
              <AddRecipeToCookbook onAdded={refresh} />
              <ImportCookbooks onImported={refresh} />
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
