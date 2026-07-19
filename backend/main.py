from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import todos
import auth
from database import create_all_database_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize the tables 
    create_all_database_tables() 
    yield
    print("application shutting down")

app = FastAPI(
    title="todos app", 
    version="1.0", 
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'], 
    allow_headers=["*"], 
    expose_headers=["*"]
)

@app.get("/")
def root(): 
    return {"message": "welcome to todos app"}

@app.get("/health")
def health_check(): 
    return {"status": "healthy"}

app.include_router(todos.router)
app.include_router(auth.router)

if __name__ == "__main__": 
    import uvicorn 
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )