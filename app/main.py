from fastapi import FastAPI
from app.routers import tasks_routes, users_routes
from app.database.connection import engine, Base
from app.models import tasks_model, user_model

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(tasks_routes.router)
app.include_router(users_routes.router)


@app.get("/")
async def root():
    return "API rodando"
