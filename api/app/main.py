from fastapi import FastAPI

from app.routes.users import router as users_router
from app.routes.posts import router as posts_router

app = FastAPI()

app.include_router(users_router)
app.include_router(posts_router)