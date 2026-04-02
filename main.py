from fastapi import FastAPI,Request
from app.database import engine, Base
from app.api.endpoints import records
from fastapi.responses import JSONResponse
from app.api.endpoints import auth


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Dashboard API")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred.", "detail": str(exc)},
    )
app.include_router(records.router, prefix="/records", tags=["Financial Records"])
app.include_router(auth.router, tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Finance Dashboard API"}
