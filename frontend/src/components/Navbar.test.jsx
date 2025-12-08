import { test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { MemoryRouter } from "react-router-dom";
import Navbar from "./Navbar";

test("shows the app logo text in the navbar", () => {
    render(
        <MemoryRouter>
            <Navbar />
        </MemoryRouter>
    );

    expect(screen.getByText(/recipe search/i)).toBeInTheDocument();
});

test("shows Dashboard and Search navigation links", () => {
    render(
        <MemoryRouter>
            <Navbar />
        </MemoryRouter>
    );

    const dashboardLink = screen.getAllByText("📊 Dashboard")[0];
    const searchLink = screen.getAllByText("🔍 Search")[0];

    expect(dashboardLink).toBeInTheDocument();
    expect(searchLink).toBeInTheDocument();
});

test("highlights Dashboard as active on home route", () => {
    render(
        <MemoryRouter initialEntries={["/"]}>
            <Navbar />
        </MemoryRouter>
    );

    const dashboardLink = screen.getAllByText("📊 Dashboard")[0];
    const searchLink = screen.getAllByText("🔍 Search")[0];

    expect(dashboardLink).toHaveClass("active");
    expect(searchLink).not.toHaveClass("active");
});