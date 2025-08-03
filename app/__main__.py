from fastapi import FastAPI
from app.handlers.router import router

app = FastAPI()
app.include_router(router)
