from fastapi import FastAPI

from .api.router import main_router
from .settings import settings
app = FastAPI()
app.include_router(main_router, prefix=settings.API_URL)

@app.get("/")
async def root():
    return {"message": "ok"}

