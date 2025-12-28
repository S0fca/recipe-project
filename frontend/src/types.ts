export type Recipe = {
  id: number;
  title: string;
  description: string;
  difficulty: Difficulty;
  is_vegetarian: boolean;
  created_at: string;
  ingredients: Ingredient[];
};

export type Ingredient = {
  id: number | null;
  name: string;
  amount: number;
  unit: string;
}

export type Difficulty = "easy" | "medium" | "hard";

export interface IngredientInput {
  name: string;
  amount: number;
  unit: string;
}

export interface Cookbook {
  id: number;
  name: string;
  description: string;
  recipe_count: number;
}
