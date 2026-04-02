from fastapi import FastAPI
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Dashboard API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Finance Dashboard API"}
