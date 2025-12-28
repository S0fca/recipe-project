import './App.css'
import RecipeList from "./components/RecipeList.tsx";
import AddRecipeForm from "./components/AddRecipeForm.tsx";

function App() {

  return (
    <>
        <RecipeList />
        <AddRecipeForm onRecipeAdded={() => window.location.reload()} />
    </>
  )
}

export default App
