// Mock data for recipes
const mockRecipes = [
  {
    id: 1,
    title: 'Classic Borscht',
    description: 'Traditional Ukrainian beet soup',
    ingredients: ['beet', 'cabbage', 'potato', 'meat', 'onion', 'carrot'],
    cookingTime: 90,
    difficulty: 'medium',
    imageUrl: 'https://via.placeholder.com/300x200?text=Borscht'
  },
  {
    id: 2,
    title: 'Pasta Carbonara',
    description: 'Italian pasta with bacon and creamy sauce',
    ingredients: ['spaghetti', 'bacon', 'eggs', 'parmesan', 'garlic'],
    cookingTime: 30,
    difficulty: 'easy',
    imageUrl: 'https://via.placeholder.com/300x200?text=Carbonara'
  },
  {
    id: 3,
    title: 'Greek Salad',
    description: 'Fresh salad with feta and olives',
    ingredients: ['tomatoes', 'cucumbers', 'feta', 'olives', 'onion', 'olive oil'],
    cookingTime: 15,
    difficulty: 'easy',
    imageUrl: 'https://via.placeholder.com/300x200?text=Greek+Salad'
  },
  {
    id: 4,
    title: 'Chicken Teriyaki',
    description: 'Japanese chicken in a sweet sauce',
    ingredients: ['chicken', 'soy sauce', 'honey', 'ginger', 'garlic', 'rice'],
    cookingTime: 45,
    difficulty: 'medium',
    imageUrl: 'https://via.placeholder.com/300x200?text=Teriyaki'
  },
  {
    id: 5,
    title: 'Pizza Margherita',
    description: 'Classic Italian pizza',
    ingredients: ['dough', 'tomato sauce', 'mozzarella', 'basil', 'olive oil'],
    cookingTime: 30,
    difficulty: 'medium',
    imageUrl: 'https://via.placeholder.com/300x200?text=Margherita'
  },
  {
    id: 6,
    title: 'Tiramisu',
    description: 'Italian dessert with coffee and mascarpone',
    ingredients: ['mascarpone', 'ladyfingers', 'coffee', 'eggs', 'sugar', 'cocoa'],
    cookingTime: 40,
    difficulty: 'hard',
    imageUrl: 'https://via.placeholder.com/300x200?text=Tiramisu'
  }
];

// Simulate network delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// API functions
export const recipesAPI = {
  // Get all recipes
  getAllRecipes: async () => {
    await delay(300);
    console.log('API: Fetching all recipes');
    return {
      success: true,
      data: mockRecipes
    };
  },

  // Search recipes by query
  searchRecipes: async (query) => {
    await delay(500);
    console.log('API: Searching recipes with query:', query);
    
    if (!query || query.trim() === '') {
      return {
        success: true,
        data: mockRecipes
      };
    }

    const lowerQuery = query.toLowerCase();
    const filtered = mockRecipes.filter(recipe => 
      recipe.title.toLowerCase().includes(lowerQuery) ||
      recipe.description.toLowerCase().includes(lowerQuery) ||
      recipe.ingredients.some(ing => ing.toLowerCase().includes(lowerQuery))
    );

    return {
      success: true,
      data: filtered,
      query: query
    };
  },

  // Get a recipe by ID
  getRecipeById: async (id) => {
    await delay(300);
    console.log('API: Fetching recipe with ID:', id);
    
    const recipe = mockRecipes.find(r => r.id === parseInt(id));
    
    if (recipe) {
      return {
        success: true,
        data: recipe
      };
    } else {
      return {
        success: false,
        error: 'Recipe not found'
      };
    }
  },

  // Add a new recipe (currently just logs)
  addRecipe: async (recipeData) => {
    await delay(500);
    console.log('API: Adding new recipe:', recipeData);
    
    // In future this will POST to a backend
    // For now just return success
    return {
      success: true,
      message: 'Recipe will be added after backend is connected',
      data: {
        id: Date.now(),
        ...recipeData
      }
    };
  },

  // Delete a recipe
  deleteRecipe: async (id) => {
    await delay(300);
    console.log('API: Deleting recipe with ID:', id);
    
    return {
      success: true,
      message: 'Recipe will be deleted after backend is connected'
    };
  }
};

// Export mock data for development
export { mockRecipes };
