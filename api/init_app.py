from fastapi import FastAPI
from api.routers import category, documents
import uvicorn

app = FastAPI()

app.include_router(category.router, prefix="/category", tags=["category"])
app.include_router(documents.router, prefix="/document", tags=["document"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
