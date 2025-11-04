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

  return (
    <div className="recipe-card">
      <div className="recipe-image">
        <img src={recipe.imageUrl} alt={recipe.title} />
        <div 
          className="difficulty-badge"
          style={{ backgroundColor: getDifficultyColor(recipe.difficulty) }}
        >
          {recipe.difficulty}
        </div>
      </div>
      
      <div className="recipe-content">
        <h3 className="recipe-title">{recipe.title}</h3>
        <p className="recipe-description">{recipe.description}</p>
        
        <div className="recipe-meta">
          <div className="meta-item">
            <span className="icon">⏱️</span>
            <span>{recipe.cookingTime} min</span>
          </div>
          <div className="meta-item">
            <span className="icon">🥘</span>
            <span>{recipe.ingredients.length} ingr.</span>
          </div>
        </div>

        <div className="recipe-ingredients">
          <strong>Ingredients:</strong>
          <div className="ingredients-tags">
            {recipe.ingredients.slice(0, 4).map((ingredient, index) => (
              <span key={index} className="ingredient-tag">
                {ingredient}
              </span>
            ))}
            {recipe.ingredients.length > 4 && (
              <span className="ingredient-tag more">
                +{recipe.ingredients.length - 4}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default RecipeCard;
