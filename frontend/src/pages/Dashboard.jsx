import { useState, useEffect } from 'react';
import { recipesAPI } from '../api/recipes';
import RecipeCard from '../components/RecipeCard';
import '../styles/Dashboard.css';

function Dashboard() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // pagination
  const itemsPerPage = 15;
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    loadRecipes();
  }, []);

  const loadRecipes = async () => {
    try {
      setLoading(true);
      const response = await recipesAPI.getAllRecipes();
      if (response.success) {
        setRecipes(response.data);
      } else {
        setError('Failed to load recipes');
      }
    } catch (err) {
      setError('Error loading recipes');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // pagination helpers
  const totalPages = Math.max(1, Math.ceil(recipes.length / itemsPerPage));
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const visibleRecipes = recipes.slice(startIndex, endIndex);

  const goToPage = (page) => {
    const p = Math.min(Math.max(1, page), totalPages);
    setCurrentPage(p);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const prevPage = () => goToPage(currentPage - 1);
  const nextPage = () => goToPage(currentPage + 1);

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading">Loading recipes...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard">
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>All Recipes</h1>
        <p className="subtitle">Recipes found: {recipes.length}</p>
      </div>

      <div className="recipes-grid">
        {visibleRecipes.map(recipe => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>

      <div className="pagination">
        <button onClick={prevPage} disabled={currentPage === 1}>
          Previous
        </button>

        {/* simple page numbers - limit long lists */}
        {Array.from({ length: totalPages }, (_, i) => i + 1)
          .slice(
            Math.max(0, currentPage - 3),
            Math.min(totalPages, currentPage + 2)
          )
          .map((p) => (
            <button
              key={p}
              className={p === currentPage ? 'active' : ''}
              onClick={() => goToPage(p)}
            >
              {p}
            </button>
          ))}

        <button onClick={nextPage} disabled={currentPage === totalPages}>
          Next
        </button>
      </div>
    </div>
  );
}

export default Dashboard;