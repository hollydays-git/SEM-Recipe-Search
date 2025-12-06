const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

const normalizeRecipe = (recipe = {}) => ({
  id: recipe.id,
  title: recipe.title,
  description: recipe.description || '',
  imageUrl: recipe.cover_url || recipe.image_url || '',
  difficulty: recipe.difficulty || 'medium',
  cookingTime: recipe.cooking_time ?? recipe.cookingTime ?? null,
  popularity: recipe.popularity ?? null,
  ingredients: Array.isArray(recipe.ingredients) ? recipe.ingredients : [],
});

export const recipesAPI = {
  getAllRecipes: async ({ limit = 50, offset = 0 } = {}) => {
    console.log('API: Fetching recipes list');
    try {
      const response = await fetch(`${API_BASE_URL}/recipes?limit=${limit}&offset=${offset}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        success: true,
        data: (data.items || []).map(normalizeRecipe),
        pagination: { limit: data.limit, offset: data.offset }
      };
    } catch (error) {
      console.error('API Error:', error);
      return { success: false, error: error.message };
    }
  },

  searchRecipes: async (query) => {
    console.log('API: Searching recipes with query:', query);

    if (!query || query.trim() === '') {
      return recipesAPI.getAllRecipes();
    }

    try {
      const response = await fetch(`${API_BASE_URL}/recipes/match?query=${encodeURIComponent(query)}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        success: true,
        data: (data.results || []).map(normalizeRecipe),
        query: data.query
      };
    } catch (error) {
      console.error('API Error:', error);
      return { success: false, error: error.message };
    }
  },

  getRecipeById: async (id) => {
    console.log('API: Fetching recipe with ID:', id);
    try {
      const response = await fetch(`${API_BASE_URL}/recipes/${id}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        success: true,
        data: {
          ...normalizeRecipe(data),
          steps: data.steps || []
        }
      };
    } catch (error) {
      console.error('API Error:', error);
      return { success: false, error: error.message };
    }
  },

  getSimilarRecipes: async (id, { limit = 5 } = {}) => {
    console.log('API: Fetching similar recipes for ID:', id);
    try {
      const response = await fetch(`${API_BASE_URL}/recipes/${id}/similar?limit=${limit}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const items = (data.items || []).map((item) => {
        const normalized = normalizeRecipe(item);
        if (typeof item.score !== 'undefined') {
          normalized.score = item.score;
        }
        return normalized;
      });

      return { success: true, data: items };
    } catch (error) {
      console.error('API Error:', error);
      return { success: false, error: error.message };
    }
  },

  // Add a new recipe
  addRecipe: async (recipeData) => {
    console.log('API: Adding new recipe:', recipeData);
    // Placeholder: Backend might not have POST /recipes yet based on provided info
    // Returning mock success for now to prevent UI breaking if this feature is used
    return {
      success: true,
      message: 'Backend add endpoint not yet implemented',
      data: {
        id: Date.now(),
        ...recipeData
      }
    };
  },

  // Delete a recipe
  deleteRecipe: async (id) => {
    console.log('API: Deleting recipe with ID:', id);
    // Placeholder
    return {
      success: true,
      message: 'Backend delete endpoint not yet implemented'
    };
  }
};
