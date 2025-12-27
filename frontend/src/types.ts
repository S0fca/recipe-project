export type Recipe = {
  id: number;
  title: string;
  description: string;
  difficulty: "easy" | "medium" | "hard";
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

