"""FastAPI application entry point for RecipePricer API."""

from fastapi import FastAPI

from routers.recipe_router import router

app = FastAPI(
    title="RecipePricer API",
    description="Calculate recipe costs with yield and profit margin",
    version="0.1.0",
)

app.include_router(router)