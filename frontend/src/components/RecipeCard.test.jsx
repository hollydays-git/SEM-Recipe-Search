import { test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import RecipeCard from "./RecipeCard";

const exampleRecipe = {
    title: "Test Dish",
    description: "A delicious test meal",
    imageUrl: "https://example.com/test.jpg",
    cookingTime: 45,
    ingredients: ["Salt", "Pepper", "Oil", "Garlic", "Onion"],
    difficulty: "medium",
};

test("displays recipe title and description", () => {
    render(<RecipeCard recipe={exampleRecipe} />);

    expect(screen.getByText("Test Dish")).toBeInTheDocument();
    expect(screen.getByText("A delicious test meal")).toBeInTheDocument();
});