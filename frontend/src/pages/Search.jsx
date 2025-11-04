import { useState } from 'react';
import { recipesAPI } from '../api/recipes';
import RecipeCard from '../components/RecipeCard';
import '../styles/Search.css';

function Search() {
  const [searchQuery, setSearchQuery] = useState('');
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setSearched(true);
      const response = await recipesAPI.searchRecipes(searchQuery);
      if (response.success) {
        setRecipes(response.data);
      }
    } catch (err) {
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-page">
      <div className="search-header">
        <h1>Search Recipes</h1>
        <p className="subtitle">Find a recipe by title, description, or ingredients</p>
      </div>

      <form className="search-form" onSubmit={handleSearch}>
        <div className="search-input-wrapper">
          <input
            type="text"
            className="search-input"
            placeholder="e.g.: chicken, pasta, salad..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button type="submit" className="search-button">
            🔍 Search
          </button>
        </div>
      </form>

      {loading && (
        <div className="loading">Searching recipes...</div>
      )}

      {!loading && searched && (
        <div className="search-results">
          <h2>Search Results</h2>
          {recipes.length > 0 ? (
            <>
              <p className="results-count">Recipes found: {recipes.length}</p>
              <div className="recipes-grid">
                {recipes.map(recipe => (
                  <RecipeCard key={recipe.id} recipe={recipe} />
                ))}
              </div>
            </>
          ) : (
            <div className="no-results">
              <p>😕 Recipes not found</p>
              <p>Try adjusting your query</p>
            </div>
          )}
        </div>
      )}

      {!searched && (
        <div className="search-tips">
          <h3>💡 Search tips:</h3>
          <ul>
            <li>Enter the dish name (e.g.: "borscht", "pizza")</li>
            <li>Specify an ingredient (e.g.: "chicken", "tomatoes")</li>
            <li>You can search by any word from the description</li>
          </ul>
        </div>
      )}
    </div>
  );
}

export default Search;
