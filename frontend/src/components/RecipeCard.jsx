import { Link } from 'react-router-dom';
import '../styles/RecipeCard.css';

function RecipeCard({ recipe }) {
  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return '#4caf50';
      case 'medium': return '#ff9800';
      case 'hard': return '#f44336';
      default: return '#757575';
    }
  };

  const getDifficultyLabel = (difficulty) => {
    if (!difficulty) return '';
    return difficulty.charAt(0).toUpperCase() + difficulty.slice(1);
  };

  const ingredients = Array.isArray(recipe.ingredients) ? recipe.ingredients : [];
  const cookingTime = recipe.cookingTime ?? '-';
  const imageSrc = recipe.imageUrl || recipe.cover_url || 'https://via.placeholder.com/400x250?text=Recipe';

  const cardBody = (
    <div className="recipe-card">
      <div className="recipe-image">
        <img src={imageSrc} alt={recipe.title} />
        <div
          className="difficulty-badge"
          style={{ backgroundColor: getDifficultyColor(recipe.difficulty) }}
        >
          {getDifficultyLabel(recipe.difficulty)}
        </div>
      </div>

      <div className="recipe-content">
        <h3 className="recipe-title">{recipe.title}</h3>
        <p className="recipe-description">{recipe.description || 'No description available yet.'}</p>

        <div className="recipe-meta">
          <div className="meta-item">
            <span className="icon">⏱️</span>
            <span>{cookingTime ? `${cookingTime} min` : 'N/A'}</span>
          </div>
          <div className="meta-item">
            <span className="icon">🥘</span>
            <span>{ingredients.length} ingr.</span>
          </div>
        </div>

        <div className="recipe-ingredients">
          <strong>Ingredients:</strong>
          <div className="ingredients-tags">
            {ingredients.slice(0, 4).map((ingredient, index) => (
              <span key={index} className="ingredient-tag">
                {ingredient}
              </span>
            ))}
            {ingredients.length > 4 && (
              <span className="ingredient-tag more">
                +{ingredients.length - 4}
              </span>
            )}
            {ingredients.length === 0 && (
              <span className="ingredient-tag placeholder">
                Ingredients coming soon
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  if (!recipe.id) {
    return cardBody;
  }

  return (
    <Link to={`/recipes/${recipe.id}`} className="recipe-card-link">
      {cardBody}
    </Link>
  );
}

export default RecipeCard;
