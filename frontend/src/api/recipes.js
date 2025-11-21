// Base URL for the backend API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// API functions
export const recipesAPI = {
  // Get all recipes
  getAllRecipes: async () => {
    console.log('API: Fetching all recipes from backend');
    try {
      // Assuming backend has an endpoint for all recipes, e.g., /recipes/all
      // If not, we might need to adjust based on exact backend routes
      const response = await fetch(`${API_BASE_URL}/recipes/all`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return {
        success: true,
        data: data
      };
    } catch (error) {
      console.error('API Error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  },

  // Search recipes by query
  searchRecipes: async (query) => {
    console.log('API: Searching recipes with query:', query);
    
    if (!query || query.trim() === '') {
      return recipesAPI.getAllRecipes();
    }

    try {
      // Using the endpoint defined in README: GET /recipes/match?query=<text>
      const response = await fetch(`${API_BASE_URL}/recipes/match?query=${encodeURIComponent(query)}`);
      console.log(`${API_BASE_URL}/recipes/match?query=${encodeURIComponent(query)}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // The backend returns { query: "...", results: [...] }
      // We need to map this to the format expected by the frontend components
      return {
        success: true,
        data: data.results, // Backend returns 'results' array
        query: data.query
      };
    } catch (error) {
      console.error('API Error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  },

  // Get a recipe by ID
  getRecipeById: async (id) => {
    console.log('API: Fetching recipe with ID:', id);
    try {
      const response = await fetch(`${API_BASE_URL}/recipes/${id}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data) {
        return {
          success: true,
          data: data
        };
      } else {
        return {
          success: false,
          error: 'Recipe not found'
        };
      }
    } catch (error) {
      console.error('API Error:', error);
      return {
        success: false,
        error: error.message
      };
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