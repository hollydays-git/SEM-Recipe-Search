# SEM-Recipe-Search
Backend description
=======
How to run

Make sure you have Python 3.10+ and virtualenv installed.

From the backend folder:

pip install -r requirements.txt
uvicorn app.main:app --reload


The API will start on http://127.0.0.1:8000.

---------------------

- `GET /recipes` – paginated list for the dashboard.
- `GET /recipes/{id}` – detailed recipe data including steps.
- `GET /recipes/search?query=...` – simple title search (ILIKE).
- `GET /recipes/match?query=...` – fuzzy Postgres search
- `GET /recipes/{id}/similar` – similar recipes based on Qdrant.
- `POST /recipes` – create recipe, store steps, and index in Qdrant.

All responses are JSON and follow the structures expected by the current React client (`frontend/src/api/recipes.js`).

---

## To Run frontend 

1. You need to install npm:
```bash
npm install
```
this will install all nessesary dependanses

2. Configure the host of the backend at the .env file according to the .env.exm file in the Frontend folder:

3. Run dev deployment:
 ```
 npm run dev
```
now the frontend will be available at http://localhost:5173


---

## Standalone ONNX embedding service

The `embedding_service/` folder contains an ONNX model and tokenizer. Install the dependencies (`pip install -r embedding_service/requirements.txt`) and run the server:

```bash
uvicorn embedding_service.main:app --host 0.0.0.0 --port 8100
```

Available endpoints:

- `GET /health` – shows the loaded ONNX model and tokenizer.
- `POST /embed` – accepts a list of texts and returns embeddings that can be inserted into Qdrant.

Query example:

```
POST http://localhost:8100/embed
{
  "texts": ["passage: Mix chicken with garlic"]
}
```

Response returns `embeddings` (list of vectors), `model` (model name) and `count` (number of returned vectors). Only `embeddings` is required for the backend to push data into Qdrant.
