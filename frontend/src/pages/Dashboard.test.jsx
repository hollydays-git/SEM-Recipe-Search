import { describe, test, expect, vi, afterEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import Dashboard from "../pages/Dashboard";

vi.mock("../components/RecipeCard", () => ({
    default: () => <div data-testid="recipe-card">Mock Recipe Card</div>,
}));

vi.mock("../api/recipes", () => ({
    recipesAPI: {
        getAllRecipes: vi.fn(),
    },
}));

describe("Dashboard Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
    });

    test("shows loading state initially", () => {
        import("../api/recipes").then(({ recipesAPI }) => {
            recipesAPI.getAllRecipes.mockReturnValue(new Promise(() => { }));
        });

        render(<Dashboard />);
        expect(screen.getByText(/loading recipes/i)).toBeInTheDocument();
    });

    test("shows error message if API fails", async () => {
        const { recipesAPI } = await import("../api/recipes");

        recipesAPI.getAllRecipes.mockResolvedValue({
            success: false,
            data: [],
        });

        render(<Dashboard />);

        await waitFor(() => {
            expect(screen.getByText(/failed to load recipes/i)).toBeInTheDocument();
        });
    });

    test("renders recipes when API succeeds", async () => {
        const { recipesAPI } = await import("../api/recipes");

        recipesAPI.getAllRecipes.mockResolvedValue({
            success: true,
            data: [
                { id: 1, title: "Recipe One" },
                { id: 2, title: "Recipe Two" },
            ],
        });

        render(<Dashboard />);

        await waitFor(() => {
            expect(screen.getByText(/recipes found: 2/i)).toBeInTheDocument();
        });

        expect(screen.getAllByTestId("recipe-card")).toHaveLength(2);
    });
});