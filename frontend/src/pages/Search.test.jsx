import { describe, test, expect, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import Search from "./Search";
import { vi } from "vitest";
import * as recipesAPI from "../api/recipes";

vi.mock("../components/RecipeCard", () => ({
    default: ({ recipe }) => (
        <div data-testid="recipe-card">{recipe?.title || "Mock Recipe Card"}</div>
    ),
}));

vi.mock("../api/recipes", () => ({
    recipesAPI: {
        searchRecipes: vi.fn(),
    },
}));

describe("Search Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
    });

    test("renders search header and input", () => {
        render(<Search />);

        expect(screen.getByText(/Search Recipes/i)).toBeInTheDocument();

        const input = screen.getAllByPlaceholderText(
            /e\.g\.: chicken, pasta, salad/i
        )[0];

        expect(input).toBeInTheDocument();
    });

    test("shows loading indicator when searching", async () => {
        recipesAPI.recipesAPI.searchRecipes.mockResolvedValue({
            success: true,
            data: [],
        });

        render(<Search />);

        const input = screen.getAllByPlaceholderText(
            /e\.g\.: chicken, pasta, salad/i
        )[0];

        fireEvent.change(input, { target: { value: "chicken" } });

        const button = screen.getAllByRole("button", { name: /search/i })[0];
        fireEvent.submit(button);

        expect(screen.getByText(/Searching recipes/i)).toBeInTheDocument();
    });

    test("shows recipe results when API returns data", async () => {
        recipesAPI.recipesAPI.searchRecipes.mockResolvedValue({
            success: true,
            data: [
                { id: 1, title: "Chicken Soup" },
                { id: 2, title: "Pasta Salad" },
            ],
        });

        render(<Search />);

        const input = screen.getAllByPlaceholderText(
            /e\.g\.: chicken, pasta, salad/i
        )[0];

        fireEvent.change(input, { target: { value: "chicken" } });

        const button = screen.getAllByRole("button", { name: /search/i })[0];
        fireEvent.submit(button);

        await waitFor(() => {
            expect(screen.getByText(/Recipes found: 2/i)).toBeInTheDocument();
        });

        expect(screen.getAllByTestId("recipe-card").length).toBe(2);
    });

    test("shows 'not found' message when API returns empty results", async () => {
        recipesAPI.recipesAPI.searchRecipes.mockResolvedValue({
            success: true,
            data: [],
        });

        render(<Search />);

        const input = screen.getAllByPlaceholderText(
            /e\.g\.: chicken, pasta, salad/i
        )[0];

        fireEvent.change(input, { target: { value: "xyz" } });

        const button = screen.getAllByRole("button", { name: /search/i })[0];
        fireEvent.submit(button);

        await waitFor(() => {
            expect(screen.getByText(/recipes not found/i)).toBeInTheDocument();
        });

        expect(screen.getByText(/try adjusting your query/i)).toBeInTheDocument();
    });
});