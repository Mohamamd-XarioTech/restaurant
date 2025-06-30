from fastapi import FastAPI, Depends
from .database import create_db_and_tables
from contextlib import asynccontextmanager
from .routers import restaurants, offers, follow, favorite, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(root_path="/restaurant", title="Xario Restaurant",
              description="Restaurant Project.",
              version="0.0.1",
              contact={
                  "name": "Mohammad Naser",
                  "email": "mohammad@xariotech.com",
              },
              license_info={
                  "name": "Xario Tech",
              }, lifespan=lifespan)

# Define a global authorization dependency for all routes

app.include_router(restaurants.router)
app.include_router(offers.router)
app.include_router(orders.router)
app.include_router(favorite.router)
app.include_router(follow.router)
