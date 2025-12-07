import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { recipesAPI } from '../api/recipes';
import RecipeCard from '../components/RecipeCard';
import '../styles/RecipeDetail.css';

function RecipeDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [recipe, setRecipe] = useState(null);
  const [similar, setSimilar] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [similarLoading, setSimilarLoading] = useState(false);

  const loadRecipe = async () => {
    if (!id) return;
    try {
      setLoading(true);
      const response = await recipesAPI.getRecipeById(id);
      if (response.success) {
        setRecipe(response.data);
        setError(null);
      } else {
        setError(response.error || 'Failed to load recipe');
      }
    } catch (err) {
      setError('Failed to load recipe');
    } finally {
      setLoading(false);
    }
  };

  const loadSimilar = async () => {
    if (!id) return;
    try {
      setSimilarLoading(true);
      const response = await recipesAPI.getSimilarRecipes(id);
      if (response.success) {
        setSimilar(response.data);
      } else {
        setSimilar([]);
      }
    } finally {
      setSimilarLoading(false);
    }
  };

  useEffect(() => {
    loadRecipe();
  }, [id]);

  useEffect(() => {
    loadSimilar();
  }, [id]);

  if (loading) {
    return <div className="recipe-detail"><div className="loading">Loading recipe...</div></div>;
  }

  if (error || !recipe) {
    return (
      <div className="recipe-detail">
        <div className="error">{error || 'Recipe not found'}</div>
        <button type="button" className="button-outline" onClick={() => navigate(-1)}>
          ← Back
        </button>
      </div>
    );
  }

  const ingredients = Array.isArray(recipe.ingredients) ? recipe.ingredients : [];

  return (
    <div className="recipe-detail">
      <div className="recipe-detail-actions">
        <button type="button" className="button-outline" onClick={() => navigate(-1)}>
          ← Back
        </button>
      </div>

      <div className="recipe-detail-header">
        <div className="recipe-detail-info">
          <h1>{recipe.title}</h1>
          <p className="difficulty">Difficulty: {recipe.difficulty}</p>
          {recipe.cookingTime && (
            <p className="time">Cooking time: {recipe.cookingTime} min</p>
          )}
          {ingredients.length > 0 && (
            <div className="recipe-detail-ingredients">
              <h4>Ingredients</h4>
              <ul>
                {ingredients.map((ingredient, index) => (
                  <li key={index}>{ingredient}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
        <div className="recipe-detail-image compact">
          <img src={recipe.imageUrl || recipe.cover_url || 'https://via.placeholder.com/600x400?text=Recipe'} alt={recipe.title} />
        </div>
      </div>

      <div className="recipe-steps">
        <h2>Instructions</h2>
        {recipe.steps && recipe.steps.length > 0 ? (
          recipe.steps.map((step) => (
            <div key={step.step_number} className="recipe-step">
              <h3>Step {step.step_number}</h3>
              <div className="step-blocks">
                {step.blocks.map((block, index) => (
                  block.type === 'text' ? (
                    <p key={index} className="step-text">{block.value}</p>
                  ) : (
                    <img key={index} src={block.value} alt={`Step ${step.step_number}`} className="step-image" />
                  )
                ))}
              </div>
            </div>
          ))
        ) : (
          <p>No steps available for this recipe yet.</p>
        )}
      </div>

      <div className="recipe-similar">
        <div className="recipe-similar-header">
          <h2>Similar recipes</h2>
          <button type="button" className="button-outline" onClick={loadSimilar}>
            Refresh
          </button>
        </div>
        {similarLoading ? (
          <div className="loading">Loading recommendations...</div>
        ) : similar.length > 0 ? (
          <div className="recipes-grid">
            {similar.map((item) => (
              <RecipeCard key={item.id} recipe={item} />
            ))}
          </div>
        ) : (
          <p>No similar recipes found yet.</p>
        )}
      </div>
    </div>
  );
}

export default RecipeDetail;
