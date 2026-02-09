from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import admin_router, user_router
from .settings import settings

app = FastAPI()
app.include_router(user_router.router, prefix=settings.API_URL, tags=["Пользователь"])
app.include_router(
    admin_router.router, prefix=settings.API_URL, tags=["Админ/Редактор"]
)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://0.0.0.0:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "ok"}
