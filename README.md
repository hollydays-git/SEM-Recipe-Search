# SEM-Recipe-Search
Search for recipes by meaning, not just by words.
=======
How to run

Make sure you have Python 3.10+ and virtualenv installed.

From the backend folder:

pip install -r requirements.txt
uvicorn app.main:app --reload


The API will start on http://127.0.0.1:8000.

---------------------

Test Qdrant connection

GET /test-qdrant/


→ Returns Qdrant collections, helps to check if backend is connected to DB.

Search recipes

GET /recipes/match?query=<text>


Example:

GET /recipes/match?query=chicken+garlic


→ Returns JSON with similar recipes from the vector database:

{
  "query": "chicken garlic",
  "results": [
    {
      "id": 123,
      "score": 0.89,
      "recipe_name": "Spicy Garlic Chicken",
      "ingredients": "...",
      "instructions": "...",
      "image_url": "https://supabase.co/storage/images/..."
    }
  ]
}


---

To Run frontend 

# You need to install npm
# Install dependencies npm install
# Configure the host of the backend at the .env file according to the .env.exm file in the Frontend folder
# Run dev deployment npm run dev 
# the frontend will be available at http://localhost:5173