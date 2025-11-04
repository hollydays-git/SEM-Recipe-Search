import { useState, useEffect } from 'react';
import { recipesAPI } from '../api/recipes';
import RecipeCard from '../components/RecipeCard';
import '../styles/Dashboard.css';

function Dashboard() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
        {recipes.map(recipe => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>
    </div>
  );
}

export default Dashboard;
